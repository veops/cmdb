# -*- coding:utf-8 -*- 


import json

import redis_lock
from flask import current_app
from flask_login import login_user

import api.lib.cmdb.ci
from api.extensions import celery
from api.extensions import db
from api.extensions import es
from api.extensions import rd
from api.lib.cmdb.cache import CITypeAttributesCache
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION2
from api.lib.cmdb.perms import CIFilterPermsCRUD
from api.lib.decorator import flush_db
from api.lib.decorator import reconnect_db
from api.lib.perm.acl.cache import UserCache
from api.lib.utils import handle_arg_list
from api.models.cmdb import CI
from api.models.cmdb import CIRelation
from api.models.cmdb import CITypeAttribute


@celery.task(name="cmdb.ci_cache", queue=CMDB_QUEUE)
@flush_db
@reconnect_db
def ci_cache(ci_id, operate_type, record_id):
    from api.lib.cmdb.ci import CITriggerManager
    from api.lib.cmdb.ci import CIRelationManager

    m = api.lib.cmdb.ci.CIManager()
    ci_dict = m.get_ci_by_id_from_db(ci_id, need_children=False, use_master=False)

    if current_app.config.get("USE_ES"):
        es.create_or_update(ci_id, ci_dict)
    else:
        rd.create_or_update({ci_id: json.dumps(ci_dict)}, REDIS_PREFIX_CI)

    current_app.logger.info("{0} flush..........".format(ci_id))

    if operate_type:
        current_app.test_request_context().push()
        login_user(UserCache.get('worker'))

        CITriggerManager.fire(operate_type, ci_dict, record_id)

    ci_dict and CIRelationManager.build_by_attribute(ci_dict)


@celery.task(name="cmdb.rebuild_relation_for_attribute_changed", queue=CMDB_QUEUE)
@reconnect_db
def rebuild_relation_for_attribute_changed(ci_type_relation):
    from api.lib.cmdb.ci import CIRelationManager

    CIRelationManager.rebuild_all_by_attribute(ci_type_relation)


@celery.task(name="cmdb.batch_ci_cache", queue=CMDB_QUEUE)
@flush_db
@reconnect_db
def batch_ci_cache(ci_ids, ):  # only for attribute change index
    for ci_id in ci_ids:
        m = api.lib.cmdb.ci.CIManager()
        ci_dict = m.get_ci_by_id_from_db(ci_id, need_children=False, use_master=False)

        if current_app.config.get("USE_ES"):
            es.create_or_update(ci_id, ci_dict)
        else:
            rd.create_or_update({ci_id: json.dumps(ci_dict)}, REDIS_PREFIX_CI)

        current_app.logger.info("{0} flush..........".format(ci_id))


@celery.task(name="cmdb.ci_delete", queue=CMDB_QUEUE)
@reconnect_db
def ci_delete(ci_id):
    current_app.logger.info(ci_id)

    if current_app.config.get("USE_ES"):
        es.delete(ci_id)
    else:
        rd.delete(ci_id, REDIS_PREFIX_CI)

    current_app.logger.info("{0} delete..........".format(ci_id))


@celery.task(name="cmdb.delete_id_filter", queue=CMDB_QUEUE)
@reconnect_db
def delete_id_filter(ci_id):
    CIFilterPermsCRUD().delete_id_filter_by_ci_id(ci_id)


@celery.task(name="cmdb.ci_delete_trigger", queue=CMDB_QUEUE)
@reconnect_db
def ci_delete_trigger(trigger, operate_type, ci_dict):
    current_app.logger.info('delete ci {} trigger'.format(ci_dict['_id']))
    from api.lib.cmdb.ci import CITriggerManager

    current_app.test_request_context().push()
    login_user(UserCache.get('worker'))

    CITriggerManager.fire_by_trigger(trigger, operate_type, ci_dict)


@celery.task(name="cmdb.ci_relation_cache", queue=CMDB_QUEUE)
@flush_db
@reconnect_db
def ci_relation_cache(parent_id, child_id, ancestor_ids):
    with redis_lock.Lock(rd.r, "CIRelation_{}".format(parent_id)):
        if ancestor_ids is None:
            children = rd.get([parent_id], REDIS_PREFIX_CI_RELATION)[0]
            children = json.loads(children) if children is not None else {}

            cr = CIRelation.get_by(first_ci_id=parent_id, second_ci_id=child_id, ancestor_ids=ancestor_ids,
                                   first=True, to_dict=False)
            if str(child_id) not in children:
                children[str(child_id)] = cr.second_ci.type_id

            rd.create_or_update({parent_id: json.dumps(children)}, REDIS_PREFIX_CI_RELATION)

        else:
            key = "{},{}".format(ancestor_ids, parent_id)
            grandson = rd.get([key], REDIS_PREFIX_CI_RELATION2)[0]
            grandson = json.loads(grandson) if grandson is not None else {}

            cr = CIRelation.get_by(first_ci_id=parent_id, second_ci_id=child_id, ancestor_ids=ancestor_ids,
                                   first=True, to_dict=False)
            if cr and str(cr.second_ci_id) not in grandson:
                grandson[str(cr.second_ci_id)] = cr.second_ci.type_id

            rd.create_or_update({key: json.dumps(grandson)}, REDIS_PREFIX_CI_RELATION2)

    current_app.logger.info("ADD ci relation cache: {0} -> {1}".format(parent_id, child_id))


@celery.task(name="cmdb.ci_relation_add", queue=CMDB_QUEUE)
@flush_db
@reconnect_db
def ci_relation_add(parent_dict, child_id, uid):
    """
    :param parent_dict: key is '$parent_model.attr_name'
    :param child_id:
    :param uid:
    :return:
    """
    from api.lib.cmdb.ci import CIRelationManager
    from api.lib.cmdb.ci_type import CITypeAttributeManager
    from api.lib.cmdb.search import SearchError
    from api.lib.cmdb.search.ci import search

    current_app.test_request_context().push()
    login_user(UserCache.get(uid))

    for parent in parent_dict:
        parent_ci_type_name, _attr_name = parent.strip()[1:].split('.', 1)
        attr_name = CITypeAttributeManager.get_attr_name(parent_ci_type_name, _attr_name)
        if attr_name is None:
            current_app.logger.warning("attr name {} does not exist".format(_attr_name))
            continue

        parent_dict[parent] = handle_arg_list(parent_dict[parent])
        for v in parent_dict[parent]:
            query = "_type:{},{}:{}".format(parent_ci_type_name, attr_name, v)
            s = search(query)
            try:
                response, _, _, _, _, _ = s.search()
            except SearchError as e:
                current_app.logger.error('ci relation add failed: {}'.format(e))
                continue

            for ci in response:
                try:
                    CIRelationManager.add(ci['_id'], child_id)
                    ci_relation_cache(ci['_id'], child_id)
                except Exception as e:
                    current_app.logger.warning(e)
                finally:
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()


@celery.task(name="cmdb.ci_relation_delete", queue=CMDB_QUEUE)
@reconnect_db
def ci_relation_delete(parent_id, child_id, ancestor_ids):
    with redis_lock.Lock(rd.r, "CIRelation_{}".format(parent_id)):
        if ancestor_ids is None:
            children = rd.get([parent_id], REDIS_PREFIX_CI_RELATION)[0]
            children = json.loads(children) if children is not None else {}

            if str(child_id) in children:
                children.pop(str(child_id))

            rd.create_or_update({parent_id: json.dumps(children)}, REDIS_PREFIX_CI_RELATION)

        else:
            key = "{},{}".format(ancestor_ids, parent_id)
            grandson = rd.get([key], REDIS_PREFIX_CI_RELATION2)[0]
            grandson = json.loads(grandson) if grandson is not None else {}

            if str(child_id) in grandson:
                grandson.pop(str(child_id))

            rd.create_or_update({key: json.dumps(grandson)}, REDIS_PREFIX_CI_RELATION2)

    current_app.logger.info("DELETE ci relation cache: {0} -> {1}".format(parent_id, child_id))


@celery.task(name="cmdb.ci_type_attribute_order_rebuild", queue=CMDB_QUEUE)
@flush_db
@reconnect_db
def ci_type_attribute_order_rebuild(type_id, uid):
    current_app.logger.info('rebuild attribute order')

    from api.lib.cmdb.ci_type import CITypeAttributeGroupManager

    attrs = CITypeAttributesCache.get(type_id)
    id2attr = {attr.attr_id: attr for attr in attrs}

    current_app.test_request_context().push()
    login_user(UserCache.get(uid))

    res = CITypeAttributeGroupManager.get_by_type_id(type_id, True)
    order = 0
    for group in res:
        for _attr in group.get('attributes'):
            if order != id2attr.get(_attr['id']) and id2attr.get(_attr['id']):
                id2attr.get(_attr['id']).update(order=order)

            order += 1


@celery.task(name="cmdb.calc_computed_attribute", queue=CMDB_QUEUE)
@flush_db
@reconnect_db
def calc_computed_attribute(attr_id, uid):
    from api.lib.cmdb.ci import CIManager

    current_app.test_request_context().push()
    login_user(UserCache.get(uid))

    cim = CIManager()
    for i in CITypeAttribute.get_by(attr_id=attr_id, to_dict=False):
        cis = CI.get_by(type_id=i.type_id, to_dict=False)
        for ci in cis:
            cim.update(ci.id, {})
