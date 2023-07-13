# -*- coding:utf-8 -*-


import copy
import datetime
import json
import time

import click
from flask import current_app
from flask.cli import with_appcontext

import api.lib.cmdb.ci
from api.extensions import db
from api.extensions import rd
from api.lib.cmdb.ci_type import CITypeTriggerManager
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.exception import AbortException
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.resource import ResourceCRUD
from api.lib.perm.acl.resource import ResourceTypeCRUD
from api.lib.perm.acl.role import RoleCRUD
from api.lib.perm.acl.user import UserCRUD
from api.models.acl import App
from api.models.acl import ResourceType
from api.models.cmdb import CI
from api.models.cmdb import CIRelation
from api.models.cmdb import CIType
from api.models.cmdb import CITypeTrigger
from api.models.cmdb import PreferenceRelationView


@click.command()
@with_appcontext
def cmdb_init_cache():
    db.session.remove()

    ci_relations = CIRelation.get_by(to_dict=False)
    relations = dict()
    for cr in ci_relations:
        relations.setdefault(cr.first_ci_id, {}).update({cr.second_ci_id: cr.second_ci.type_id})
    for i in relations:
        relations[i] = json.dumps(relations[i])
    if relations:
        rd.create_or_update(relations, REDIS_PREFIX_CI_RELATION)

    if current_app.config.get("USE_ES"):
        from api.extensions import es
        from api.models.cmdb import Attribute
        from api.lib.cmdb.utils import ValueTypeMap
        attributes = Attribute.get_by(to_dict=False)
        for attr in attributes:
            other = dict()
            other['index'] = True if attr.is_index else False
            if attr.value_type == ValueTypeEnum.TEXT:
                other['analyzer'] = 'ik_max_word'
                other['search_analyzer'] = 'ik_smart'
                if attr.is_index:
                    other["fields"] = {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
            try:
                es.update_mapping(attr.name, ValueTypeMap.es_type[attr.value_type], other)
            except Exception as e:
                print(e)

    cis = CI.get_by(to_dict=False)
    for ci in cis:
        if current_app.config.get("USE_ES"):
            res = es.get_index_id(ci.id)
            if res:
                continue
        else:
            res = rd.get([ci.id], REDIS_PREFIX_CI)
            if res and list(filter(lambda x: x, res)):
                continue

        m = api.lib.cmdb.ci.CIManager()
        ci_dict = m.get_ci_by_id_from_db(ci.id, need_children=False, use_master=False)

        if current_app.config.get("USE_ES"):
            es.create(ci_dict)
        else:
            rd.create_or_update({ci.id: json.dumps(ci_dict)}, REDIS_PREFIX_CI)

    db.session.remove()


@click.command()
@with_appcontext
def cmdb_init_acl():
    _app = AppCache.get('cmdb') or App.create(name='cmdb')
    app_id = _app.id

    # 1. add resource type
    for resource_type in ResourceTypeEnum.all():
        try:
            ResourceTypeCRUD.add(app_id, resource_type, '', PermEnum.all())
        except AbortException:
            pass

    # 2. add role
    try:
        RoleCRUD.add_role(RoleEnum.CONFIG, app_id, True)
    except AbortException:
        pass
    try:
        RoleCRUD.add_role(RoleEnum.CMDB_READ_ALL, app_id, False)
    except AbortException:
        pass

    # 3. add resource and grant
    ci_types = CIType.get_by(to_dict=False)
    type_id = ResourceType.get_by(name=ResourceTypeEnum.CI, first=True, to_dict=False).id
    for ci_type in ci_types:
        try:
            ResourceCRUD.add(ci_type.name, type_id, app_id)
        except AbortException:
            pass

        ACLManager().grant_resource_to_role(ci_type.name,
                                            RoleEnum.CMDB_READ_ALL,
                                            ResourceTypeEnum.CI,
                                            [PermEnum.READ])

    relation_views = PreferenceRelationView.get_by(to_dict=False)
    type_id = ResourceType.get_by(name=ResourceTypeEnum.RELATION_VIEW, first=True, to_dict=False).id
    for view in relation_views:
        try:
            ResourceCRUD.add(view.name, type_id, app_id)
        except AbortException:
            pass

        ACLManager().grant_resource_to_role(view.name,
                                            RoleEnum.CMDB_READ_ALL,
                                            ResourceTypeEnum.RELATION_VIEW,
                                            [PermEnum.READ])


@click.command()
@click.option(
    '-u',
    '--user',
    help='username'
)
@click.option(
    '-p',
    '--password',
    help='password'
)
@click.option(
    '-m',
    '--mail',
    help='mail'
)
@with_appcontext
def add_user(user, password, mail):
    """
    create a user

    is_admin: default is False

    Example:  flask add-user -u <username> -p <password> -m <mail>
    """
    assert user is not None
    assert password is not None
    assert mail is not None
    UserCRUD.add(username=user, password=password, email=mail)


@click.command()
@click.option(
    '-u',
    '--user',
    help='username'
)
@with_appcontext
def del_user(user):
    """
    delete a user

    Example:  flask del-user -u <username>
    """
    assert user is not None
    from api.models.acl import User

    u = User.get_by(username=user, first=True, to_dict=False)
    u and UserCRUD.delete(u.uid)


@click.command()
@with_appcontext
def cmdb_counter():
    from api.lib.cmdb.cache import CMDBCounterCache

    while True:
        try:
            db.session.remove()

            CMDBCounterCache.reset()
        except:
            import traceback
            print(traceback.format_exc())

        time.sleep(60)


@click.command()
@with_appcontext
def cmdb_trigger():
    current_day = datetime.datetime.today().strftime("%Y-%m-%d")
    trigger2cis = dict()
    trigger2completed = dict()

    i = 0
    while True:
        db.session.remove()
        if datetime.datetime.today().strftime("%Y-%m-%d") != current_day:
            trigger2cis = dict()
            trigger2completed = dict()
            current_day = datetime.datetime.today().strftime("%Y-%m-%d")

        if i == 360 or i == 0:
            i = 0
            try:
                triggers = CITypeTrigger.get_by(to_dict=False)

                for trigger in triggers:
                    ready_cis = CITypeTriggerManager.waiting_cis(trigger)
                    if trigger.id not in trigger2cis:
                        trigger2cis[trigger.id] = (trigger, ready_cis)
                    else:
                        cur = trigger2cis[trigger.id]
                        cur_ci_ids = {i.ci_id for i in cur[1]}
                        trigger2cis[trigger.id] = (trigger, cur[1] + [i for i in ready_cis if i.ci_id not in cur_ci_ids
                                                                      and i.ci_id not in trigger2completed[trigger.id]])

            except Exception as e:
                print(e)

        for tid in trigger2cis:
            trigger, cis = trigger2cis[tid]
            for ci in copy.deepcopy(cis):
                if CITypeTriggerManager.trigger_notify(trigger, ci):
                    trigger2completed.setdefault(trigger.id, set()).add(ci.ci_id)

                    for _ci in cis:
                        if _ci.ci_id == ci.ci_id:
                            cis.remove(_ci)

        i += 1
        time.sleep(10)
