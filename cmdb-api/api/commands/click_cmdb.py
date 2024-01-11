# -*- coding:utf-8 -*-


import click
import copy
import datetime
import json
import requests
import time
import uuid
from flask import current_app
from flask.cli import with_appcontext
from flask_login import login_user

import api.lib.cmdb.ci
from api.extensions import db
from api.extensions import rd
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION2
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.exception import AbortException
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import UserCache
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.resource import ResourceCRUD
from api.lib.perm.acl.resource import ResourceTypeCRUD
from api.lib.perm.acl.role import RoleCRUD
from api.lib.secrets.inner import KeyManage
from api.lib.secrets.inner import global_key_threshold
from api.lib.secrets.secrets import InnerKVManger
from api.models.acl import App
from api.models.acl import ResourceType
from api.models.cmdb import Attribute
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
    relations2 = dict()
    for cr in ci_relations:
        relations.setdefault(cr.first_ci_id, {}).update({cr.second_ci_id: cr.second_ci.type_id})
        if cr.ancestor_ids:
            relations2.setdefault(cr.ancestor_ids, {}).update({cr.second_ci_id: cr.second_ci.type_id})
    for i in relations:
        relations[i] = json.dumps(relations[i])
    if relations:
        rd.create_or_update(relations, REDIS_PREFIX_CI_RELATION)
    if relations2:
        rd.create_or_update(relations2, REDIS_PREFIX_CI_RELATION2)

    es = None
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

    current_app.test_request_context().push()

    # 1. add resource type
    for resource_type in ResourceTypeEnum.all():
        try:
            perms = PermEnum.all()
            if resource_type in (ResourceTypeEnum.CI_FILTER, ResourceTypeEnum.PAGE):
                perms = [PermEnum.READ]
            elif resource_type == ResourceTypeEnum.CI_TYPE_RELATION:
                perms = [PermEnum.ADD, PermEnum.DELETE, PermEnum.GRANT]
            elif resource_type == ResourceTypeEnum.RELATION_VIEW:
                perms = [PermEnum.READ, PermEnum.UPDATE, PermEnum.DELETE, PermEnum.GRANT]

            ResourceTypeCRUD.add(app_id, resource_type, '', perms)
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
    resource_type_id = ResourceType.get_by(name=ResourceTypeEnum.CI, first=True, to_dict=False).id
    for ci_type in ci_types:
        try:
            ResourceCRUD.add(ci_type.name, resource_type_id, app_id)
        except AbortException:
            pass

        ACLManager().grant_resource_to_role(ci_type.name,
                                            RoleEnum.CMDB_READ_ALL,
                                            ResourceTypeEnum.CI,
                                            [PermEnum.READ])

    relation_views = PreferenceRelationView.get_by(to_dict=False)
    resource_type_id = ResourceType.get_by(name=ResourceTypeEnum.RELATION_VIEW, first=True, to_dict=False).id
    for view in relation_views:
        try:
            ResourceCRUD.add(view.name, resource_type_id, app_id)
        except AbortException:
            pass

        ACLManager().grant_resource_to_role(view.name,
                                            RoleEnum.CMDB_READ_ALL,
                                            ResourceTypeEnum.RELATION_VIEW,
                                            [PermEnum.READ])


@click.command()
@with_appcontext
def cmdb_counter():
    """
    Dashboard calculations
    """
    from api.lib.cmdb.cache import CMDBCounterCache

    current_app.test_request_context().push()
    if not UserCache.get('worker'):
        from api.lib.perm.acl.user import UserCRUD

        UserCRUD.add(username='worker', password=uuid.uuid4().hex, email='worker@xxx.com')

    login_user(UserCache.get('worker'))

    i = 0
    while True:
        try:
            db.session.remove()

            CMDBCounterCache.reset()

            if i % 5 == 0:
                CMDBCounterCache.flush_adc_counter()
                i = 0

            i += 1
        except:
            import traceback
            print(traceback.format_exc())

        time.sleep(60)


@click.command()
@with_appcontext
def cmdb_trigger():
    """
    Trigger execution for date attribute
    """
    from api.lib.cmdb.ci import CITriggerManager

    current_day = datetime.datetime.today().strftime("%Y-%m-%d")
    trigger2cis = dict()
    trigger2completed = dict()

    i = 0
    while True:
        try:
            db.session.remove()

            if datetime.datetime.today().strftime("%Y-%m-%d") != current_day:
                trigger2cis = dict()
                trigger2completed = dict()
                current_day = datetime.datetime.today().strftime("%Y-%m-%d")

            if i == 3 or i == 0:
                i = 0
                triggers = CITypeTrigger.get_by(to_dict=False, __func_isnot__key_attr_id=None)
                for trigger in triggers:
                    try:
                        ready_cis = CITriggerManager.waiting_cis(trigger)
                    except Exception as e:
                        print(e)
                        continue

                    if trigger.id not in trigger2cis:
                        trigger2cis[trigger.id] = (trigger, ready_cis)
                    else:
                        cur = trigger2cis[trigger.id]
                        cur_ci_ids = {i.ci_id for i in cur[1]}
                        trigger2cis[trigger.id] = (
                            trigger, cur[1] + [i for i in ready_cis if i.ci_id not in cur_ci_ids
                                               and i.ci_id not in trigger2completed.get(trigger.id, {})])

            for tid in trigger2cis:
                trigger, cis = trigger2cis[tid]
                for ci in copy.deepcopy(cis):
                    if CITriggerManager.trigger_notify(trigger, ci):
                        trigger2completed.setdefault(trigger.id, set()).add(ci.ci_id)

                        for _ci in cis:
                            if _ci.ci_id == ci.ci_id:
                                cis.remove(_ci)

            i += 1
            time.sleep(10)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            current_app.logger.error("cmdb trigger exception: {}".format(e))
            time.sleep(60)


@click.command()
@with_appcontext
def cmdb_index_table_upgrade():
    """
    Migrate data from tables c_value_integers, c_value_floats, and c_value_datetime
    """
    for attr in Attribute.get_by(to_dict=False):
        if attr.value_type not in {ValueTypeEnum.TEXT, ValueTypeEnum.JSON} and not attr.is_index:
            attr.update(is_index=True)
            AttributeCache.clean(attr)

    from api.models.cmdb import CIValueInteger, CIIndexValueInteger
    from api.models.cmdb import CIValueFloat, CIIndexValueFloat
    from api.models.cmdb import CIValueDateTime, CIIndexValueDateTime

    for i in CIValueInteger.get_by(to_dict=False):
        CIIndexValueInteger.create(ci_id=i.ci_id, attr_id=i.attr_id, value=i.value, commit=False)
        i.delete(commit=False)
    db.session.commit()

    for i in CIValueFloat.get_by(to_dict=False):
        CIIndexValueFloat.create(ci_id=i.ci_id, attr_id=i.attr_id, value=i.value, commit=False)
        i.delete(commit=False)
    db.session.commit()

    for i in CIValueDateTime.get_by(to_dict=False):
        CIIndexValueDateTime.create(ci_id=i.ci_id, attr_id=i.attr_id, value=i.value, commit=False)
        i.delete(commit=False)
    db.session.commit()


def valid_address(address):
    if not address:
        return False

    if not address.startswith(("http://127.0.0.1", "https://127.0.0.1")):
        response = {
            "message": "Address should start with http://127.0.0.1 or https://127.0.0.1",
            "status": "failed"
        }
        KeyManage.print_response(response)
        return False
    return True


@click.command()
@click.option(
    '-a',
    '--address',
    help='inner cmdb api, http://127.0.0.1:8000',
)
@with_appcontext
def cmdb_inner_secrets_init(address):
    """
    init inner secrets for password feature
    """
    res, ok = KeyManage(backend=InnerKVManger).init()
    if not ok:
        if res.get("status") == "failed":
            KeyManage.print_response(res)
            return

    token = res.get("details", {}).get("root_token", "")
    if valid_address(address):
        token = current_app.config.get("INNER_TRIGGER_TOKEN", "") if not token else token
        if not token:
            token = click.prompt(f'Enter root token', hide_input=True, confirmation_prompt=False)
        assert token is not None
        resp = requests.post("{}/api/v0.1/secrets/auto_seal".format(address.strip("/")),
                             headers={"Inner-Token": token})
        if resp.status_code == 200:
            KeyManage.print_response(resp.json())
        else:
            KeyManage.print_response({"message": resp.text or resp.status_code, "status": "failed"})
    else:
        KeyManage.print_response(res)


@click.command()
@click.option(
    '-a',
    '--address',
    help='inner cmdb api, http://127.0.0.1:8000',
    required=True,
)
@with_appcontext
def cmdb_inner_secrets_unseal(address):
    """
    unseal the secrets feature
    """
    if not valid_address(address):
        return
    address = "{}/api/v0.1/secrets/unseal".format(address.strip("/"))
    for i in range(global_key_threshold):
        token = click.prompt(f'Enter unseal token {i + 1}', hide_input=True, confirmation_prompt=False)
        assert token is not None
        resp = requests.post(address, headers={"Unseal-Token": token})
        if resp.status_code == 200:
            KeyManage.print_response(resp.json())
            if resp.json().get("status") in ["success", "skip"]:
                return
        else:
            KeyManage.print_response({"message": resp.status_code, "status": "failed"})
            return


@click.command()
@click.option(
    '-a',
    '--address',
    help='inner cmdb api, http://127.0.0.1:8000',
    required=True,
)
@click.option(
    '-k',
    '--token',
    help='root token',
    prompt=True,
    hide_input=True,
)
@with_appcontext
def cmdb_inner_secrets_seal(address, token):
    """
    seal the secrets feature
    """
    assert address is not None
    assert token is not None
    if not valid_address(address):
        return
    address = "{}/api/v0.1/secrets/seal".format(address.strip("/"))
    resp = requests.post(address, headers={
        "Inner-Token": token,
    })
    if resp.status_code == 200:
        KeyManage.print_response(resp.json())
    else:
        KeyManage.print_response({"message": resp.status_code, "status": "failed"})


@click.command()
@with_appcontext
def cmdb_password_data_migrate():
    """
    Migrate CI password data, version >= v2.3.6
    """
    from api.models.cmdb import CIIndexValueText
    from api.models.cmdb import CIValueText
    from api.lib.secrets.inner import InnerCrypt
    from api.lib.secrets.vault import VaultClient

    attrs = Attribute.get_by(to_dict=False)
    for attr in attrs:
        if attr.is_password:

            value_table = CIIndexValueText if attr.is_index else CIValueText

            failed = False
            for i in value_table.get_by(attr_id=attr.id, to_dict=False):
                if current_app.config.get("SECRETS_ENGINE", 'inner') == 'inner':
                    _, status = InnerCrypt().decrypt(i.value)
                    if status:
                        continue

                    encrypt_value, status = InnerCrypt().encrypt(i.value)
                    if status:
                        CIValueText.create(ci_id=i.ci_id, attr_id=attr.id, value=encrypt_value)
                    else:
                        failed = True
                        continue
                elif current_app.config.get("SECRETS_ENGINE") == 'vault':
                    if i.value == '******':
                        continue

                    vault = VaultClient(current_app.config.get('VAULT_URL'), current_app.config.get('VAULT_TOKEN'))
                    try:
                        vault.update("/{}/{}".format(i.ci_id, i.attr_id), dict(v=i.value))
                    except Exception as e:
                        print('save password to vault failed: {}'.format(e))
                        failed = True
                        continue
                else:
                    continue

                i.delete()

                if not failed and attr.is_index:
                    attr.update(is_index=False)


@click.command()
@with_appcontext
def cmdb_agent_init():
    """
    Initialize the agent's permissions and obtain the key and secret
    """

    from api.models.acl import User

    user = User.get_by(username="cmdb_agent", first=True, to_dict=False)
    if user is None:
        click.echo(
            click.style('user cmdb_agent does not exist, please use flask add-user to create it first', fg='red'))
        return

    # grant
    _app = AppCache.get('cmdb') or App.create(name='cmdb')
    app_id = _app.id

    ci_types = CIType.get_by(to_dict=False)
    resource_type_id = ResourceType.get_by(name=ResourceTypeEnum.CI, first=True, to_dict=False).id
    for ci_type in ci_types:
        try:
            ResourceCRUD.add(ci_type.name, resource_type_id, app_id)
        except AbortException:
            pass

        ACLManager().grant_resource_to_role(ci_type.name,
                                            "cmdb_agent",
                                            ResourceTypeEnum.CI,
                                            [PermEnum.READ, PermEnum.UPDATE, PermEnum.ADD, PermEnum.DELETE])

    click.echo("Key   : {}".format(click.style(user.key, bg='red')))
    click.echo("Secret: {}".format(click.style(user.secret, bg='red')))
