# -*- coding:utf-8 -*-
import datetime
import json
import os

from flask import abort
from flask import current_app
from flask_login import current_user
from sqlalchemy import func

from api.extensions import db
from api.lib.cmdb.auto_discovery.const import ClOUD_MAP
from api.lib.cmdb.cache import CITypeAttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.ci_type import CITypeGroupManager
from api.lib.cmdb.const import AutoDiscoveryType
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search import SearchError
from api.lib.cmdb.search.ci import search
from api.lib.mixin import DBMixin
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.acl import validate_permission
from api.lib.utils import AESCrypto
from api.models.cmdb import AutoDiscoveryCI
from api.models.cmdb import AutoDiscoveryCIType
from api.models.cmdb import AutoDiscoveryRule

PWD = os.path.abspath(os.path.dirname(__file__))


def parse_plugin_script(script):
    attributes = []
    try:
        x = compile(script, '', "exec")
        exec(x)
        unique_key = locals()['AutoDiscovery']().unique_key
        attrs = locals()['AutoDiscovery']().attributes() or []
    except Exception as e:
        return abort(400, str(e))

    if not isinstance(attrs, list):
        return abort(400, ErrFormat.adr_plugin_attributes_list_required)

    for i in attrs:
        if len(i) == 3:
            name, _type, desc = i
        elif len(i) == 2:
            name, _type = i
            desc = ""
        else:
            continue
        attributes.append(dict(name=name, type=_type, desc=desc))

    return unique_key, attributes


def check_plugin_script(**kwargs):
    kwargs['unique_key'], kwargs['attributes'] = parse_plugin_script(kwargs['plugin_script'])

    if not kwargs.get('unique_key'):
        return abort(400, ErrFormat.adr_unique_key_required)

    if not kwargs.get('attributes'):
        return abort(400, ErrFormat.adr_plugin_attributes_list_no_empty)

    return kwargs


class AutoDiscoveryRuleCRUD(DBMixin):
    cls = AutoDiscoveryRule

    @classmethod
    def get_by_name(cls, name):
        return cls.cls.get_by(name=name, first=True, to_dict=False)

    @classmethod
    def get_by_id(cls, _id):
        return cls.cls.get_by_id(_id)

    def get_by_inner(self):
        return self.cls.get_by(is_inner=True, to_dict=True)

    def import_template(self, rules):
        for rule in rules:
            rule.pop("id", None)
            rule.pop("created_at", None)
            rule.pop("updated_at", None)

            existed = self.cls.get_by(name=rule['name'], first=True, to_dict=False)
            if existed is not None:
                existed.update(**rule)
            else:
                self.cls.create(**rule)

    def _can_add(self, **kwargs):
        self.cls.get_by(name=kwargs['name']) and abort(400, ErrFormat.adr_duplicate.format(kwargs['name']))
        if kwargs.get('is_plugin') and kwargs.get('plugin_script'):
            kwargs = check_plugin_script(**kwargs)

        return kwargs

    def _can_update(self, **kwargs):
        existed = self.cls.get_by_id(kwargs['_id']) or abort(
            404, ErrFormat.adr_not_found.format("id={}".format(kwargs['_id'])))

        if 'name' in kwargs and not kwargs['name']:
            return abort(400, ErrFormat.argument_value_required.format('name'))

        if kwargs.get('name'):
            other = self.cls.get_by(name=kwargs['name'], first=True, to_dict=False)
            if other and other.id != existed.id:
                return abort(400, ErrFormat.adr_duplicate.format(kwargs['name']))

        return existed

    def update(self, _id, **kwargs):

        if kwargs.get('is_plugin') and kwargs.get('plugin_script'):
            kwargs = check_plugin_script(**kwargs)

        return super(AutoDiscoveryRuleCRUD, self).update(_id, filter_none=False, **kwargs)

    def _can_delete(self, **kwargs):
        if AutoDiscoveryCIType.get_by(adr_id=kwargs['_id'], first=True):
            return abort(400, ErrFormat.adr_referenced)

        return self._can_update(**kwargs)


class AutoDiscoveryCITypeCRUD(DBMixin):
    cls = AutoDiscoveryCIType

    @classmethod
    def get_all(cls):
        return cls.cls.get_by(to_dict=False)

    @classmethod
    def get_by_id(cls, _id):
        return cls.cls.get_by_id(_id)

    @classmethod
    def get_by_type_id(cls, type_id):
        return cls.cls.get_by(type_id=type_id, to_dict=False)

    @classmethod
    def get(cls, ci_id, oneagent_id, last_update_at=None):
        result = []
        rules = cls.cls.get_by(to_dict=True)

        for rule in rules:
            if rule.get('relation'):
                continue

            if isinstance(rule.get("extra_option"), dict) and rule['extra_option'].get('secret'):
                if not (current_user.username == "cmdb_agent" or current_user.uid == rule['uid']):
                    rule['extra_option'].pop('secret', None)
                else:
                    rule['extra_option']['secret'] = AESCrypto.decrypt(rule['extra_option']['secret'])

            if oneagent_id and rule['agent_id'] == oneagent_id:
                result.append(rule)
            elif rule['query_expr']:
                query = rule['query_expr'].lstrip('q').lstrip('=')
                s = search(query, fl=['_id'], count=1000000)
                try:
                    response, _, _, _, _, _ = s.search()
                except SearchError as e:
                    return abort(400, str(e))

                for i in (response or []):
                    if i.get('_id') == ci_id:
                        result.append(rule)
                        break
            elif not rule['agent_id'] and not rule['query_expr'] and rule['adr_id']:
                adr = AutoDiscoveryRuleCRUD.get_by_id(rule['adr_id'])
                if not adr:
                    continue
                if adr.type in (AutoDiscoveryType.SNMP, AutoDiscoveryType.HTTP):
                    continue

                if not rule['updated_at']:
                    continue

                result.append(rule)

        new_last_update_at = ""
        for i in result:
            i['adr'] = AutoDiscoveryRule.get_by_id(i['adr_id']).to_dict()
            __last_update_at = max([i['updated_at'] or "", i['created_at'] or "",
                                    i['adr']['created_at'] or "", i['adr']['updated_at'] or ""])
            if new_last_update_at < __last_update_at:
                new_last_update_at = __last_update_at

        if not last_update_at or new_last_update_at > last_update_at:
            return result, new_last_update_at
        else:
            return [], new_last_update_at

    @staticmethod
    def __valid_exec_target(agent_id, query_expr):
        _is_app_admin = is_app_admin("cmdb")
        if not agent_id and not query_expr and not _is_app_admin:
            return abort(403, ErrFormat.adt_target_all_no_permission)

        if _is_app_admin:
            return

        if agent_id and isinstance(agent_id, str) and agent_id.startswith("0x"):
            agent_id = agent_id.strip()
            q = "op_duty:{0},-rd_duty:{0},oneagent_id:{1}"

            s = search(q.format(current_user.username, agent_id.strip()))
            try:
                response, _, _, _, _, _ = s.search()
                if response:
                    return
            except SearchError as e:
                current_app.logger.warning(e)
                return abort(400, str(e))

            s = search(q.format(current_user.nickname, agent_id.strip()))
            try:
                response, _, _, _, _, _ = s.search()
                if response:
                    return
            except SearchError as e:
                current_app.logger.warning(e)
                return abort(400, str(e))

        if query_expr.strip():
            query_expr = query_expr.strip()
            if query_expr.startswith('q='):
                query_expr = query_expr[2:]

            s = search(query_expr, count=1000000)
            try:
                response, _, _, _, _, _ = s.search()
                for i in response:
                    if (current_user.username not in (i.get('rd_duty') or []) and
                            current_user.username not in (i.get('op_duty') or []) and
                            current_user.nickname not in (i.get('rd_duty') or []) and
                            current_user.nickname not in (i.get('op_duty') or [])):
                        return abort(403, ErrFormat.adt_target_expr_no_permission.format(
                            i.get("{}_name".format(i.get('ci_type')))))
            except SearchError as e:
                current_app.logger.warning(e)
                return abort(400, str(e))

    def _can_add(self, **kwargs):
        self.cls.get_by(type_id=kwargs['type_id'], adr_id=kwargs.get('adr_id') or None) and abort(
            400, ErrFormat.ad_duplicate)

        # self.__valid_exec_target(kwargs.get('agent_id'), kwargs.get('query_expr'))

        if kwargs.get('adr_id'):
            adr = AutoDiscoveryRule.get_by_id(kwargs['adr_id']) or abort(
                404, ErrFormat.adr_not_found.format("id={}".format(kwargs['adr_id'])))
            if not adr.is_plugin:
                other = self.cls.get_by(adr_id=adr.id, first=True, to_dict=False)
                if other:
                    ci_type = CITypeCache.get(other.type_id)
                    return abort(400, ErrFormat.adr_default_ref_once.format(ci_type.alias))

        if kwargs.get('is_plugin') and kwargs.get('plugin_script'):
            kwargs = check_plugin_script(**kwargs)

        if isinstance(kwargs.get('extra_option'), dict) and kwargs['extra_option'].get('secret'):
            kwargs['extra_option']['secret'] = AESCrypto.encrypt(kwargs['extra_option']['secret'])

        kwargs['uid'] = current_user.uid

        return kwargs

    def _can_update(self, **kwargs):
        existed = self.cls.get_by_id(kwargs['_id']) or abort(
            404, ErrFormat.ad_not_found.format("id={}".format(kwargs['_id'])))

        self.__valid_exec_target(kwargs.get('agent_id'), kwargs.get('query_expr'))

        if isinstance(kwargs.get('extra_option'), dict) and kwargs['extra_option'].get('secret'):
            if current_user.uid != existed.uid:
                return abort(403, ErrFormat.adt_secret_no_permission)

        return existed

    def update(self, _id, **kwargs):

        if kwargs.get('is_plugin') and kwargs.get('plugin_script'):
            kwargs = check_plugin_script(**kwargs)

        if isinstance(kwargs.get('extra_option'), dict) and kwargs['extra_option'].get('secret'):
            kwargs['extra_option']['secret'] = AESCrypto.encrypt(kwargs['extra_option']['secret'])

        return super(AutoDiscoveryCITypeCRUD, self).update(_id, filter_none=False, **kwargs)

    def _can_delete(self, **kwargs):
        if AutoDiscoveryCICRUD.get_by_adt_id(kwargs['_id']):
            return abort(400, ErrFormat.cannot_delete_adt)

        existed = self.cls.get_by_id(kwargs['_id']) or abort(
            404, ErrFormat.ad_not_found.format("id={}".format(kwargs['_id'])))

        return existed


class AutoDiscoveryCICRUD(DBMixin):
    cls = AutoDiscoveryCI

    @classmethod
    def get_by_adt_id(cls, adt_id):
        return cls.cls.get_by(adt_id=adt_id, to_dict=False)

    @classmethod
    def get_type_name(cls, adc_id):
        adc = cls.cls.get_by_id(adc_id) or abort(404, ErrFormat.adc_not_found)

        ci_type = CITypeCache.get(adc.type_id)

        return ci_type and ci_type.name

    @staticmethod
    def get_ci_types(need_other):
        result = CITypeGroupManager.get(need_other, False)
        adt = {i.type_id for i in AutoDiscoveryCITypeCRUD.get_all()}
        for item in result:
            item['ci_types'] = [i for i in (item.get('ci_types') or []) if i['id'] in adt]

        return result

    @staticmethod
    def get_attributes_by_type_id(type_id):
        from api.lib.cmdb.cache import CITypeAttributesCache
        attributes = [i[1] for i in CITypeAttributesCache.get2(type_id) or []]

        attr_names = set()
        adts = AutoDiscoveryCITypeCRUD.get_by_type_id(type_id)
        for adt in adts:
            attr_names |= set((adt.attributes or {}).values())

        return [attr.to_dict() for attr in attributes if attr.name in attr_names]

    @classmethod
    def search(cls, page, page_size, fl=None, **kwargs):
        type_id = kwargs['type_id']
        adts = AutoDiscoveryCITypeCRUD.get_by_type_id(type_id)
        if not adts:
            return 0, []
        adt2attr_map = {i.id: i.attributes or {} for i in adts}

        query = db.session.query(cls.cls).filter(cls.cls.deleted.is_(False))

        count_query = db.session.query(func.count(cls.cls.id)).filter(cls.cls.deleted.is_(False))

        for k in kwargs:
            if hasattr(cls.cls, k):
                query = query.filter(getattr(cls.cls, k) == kwargs[k])
                count_query = count_query.filter(getattr(cls.cls, k) == kwargs[k])

        query = query.order_by(cls.cls.is_accept.desc()).order_by(cls.cls.id.desc())

        result = []
        for i in query.offset((page - 1) * page_size).limit(page_size):
            item = i.to_dict()
            adt_id = item['adt_id']
            item['instance'] = {adt2attr_map[adt_id][k]: v for k, v in item.get('instance').items()
                                if (not fl or k in fl) and adt2attr_map.get(adt_id, {}).get(k)}
            result.append(item)

        numfound = query.count()

        return numfound, result

    @staticmethod
    def _get_unique_key(type_id):
        ci_type = CITypeCache.get(type_id)
        if ci_type:
            attr = CITypeAttributeCache.get(type_id, ci_type.unique_id)
            return attr and attr.name

    def _can_add(self, **kwargs):
        pass

    def upsert(self, **kwargs):

        adt = AutoDiscoveryCIType.get_by_id(kwargs['adt_id']) or abort(404, ErrFormat.adt_not_found)

        existed = self.cls.get_by(type_id=kwargs['type_id'],
                                  unique_value=kwargs.get("unique_value"),
                                  first=True, to_dict=False)
        changed = False
        if existed is not None:
            if existed.instance != kwargs['instance']:
                existed.update(filter_none=False, **kwargs)
                changed = True
        else:
            existed = self.cls.create(**kwargs)
            changed = True

        if adt.auto_accept and changed:
            try:
                self.accept(existed)
            except Exception as e:
                return abort(400, str(e))
        elif changed:
            existed.update(is_accept=False, accept_time=None, accept_by=None, filter_none=False)

        return existed

    def _can_update(self, **kwargs):
        existed = self.cls.get_by_id(kwargs['_id']) or abort(404, ErrFormat.adc_not_found)

        return existed

    def _can_delete(self, **kwargs):
        return self._can_update(**kwargs)

    def delete(self, _id):
        inst = self._can_delete(_id=_id)

        inst.delete()

        self._after_delete(inst)

        return inst

    @classmethod
    def delete2(cls, type_id, unique_value):
        existed = cls.cls.get_by(type_id=type_id, unique_value=unique_value, first=True, to_dict=False) or abort(
            404, ErrFormat.adc_not_found)

        if current_app.config.get("USE_ACL"):
            ci_type = CITypeCache.get(type_id) or abort(404, ErrFormat.ci_type_not_found)

            not is_app_admin("cmdb") and validate_permission(ci_type.name, ResourceTypeEnum.CI, PermEnum.DELETE, "cmdb")

        existed.delete()
        # TODO: delete ci

    @classmethod
    def accept(cls, adc, adc_id=None, nickname=None):
        if adc_id is not None:
            adc = cls.cls.get_by_id(adc_id) or abort(404, ErrFormat.adc_not_found)

        adt = AutoDiscoveryCITypeCRUD.get_by_id(adc.adt_id) or abort(404, ErrFormat.adt_not_found)

        ci_id = None
        if adt.attributes:
            ci_dict = {adt.attributes[k]: v for k, v in adc.instance.items() if k in adt.attributes}
            ci_id = CIManager.add(adc.type_id, is_auto_discovery=True, **ci_dict)

        relation_adts = AutoDiscoveryCIType.get_by(type_id=adt.type_id, adr_id=None, to_dict=False)
        for r_adt in relation_adts:
            if not r_adt.relation or ci_id is None:
                continue
            for ad_key in r_adt.relation:
                if not adc.instance.get(ad_key):
                    continue
                cmdb_key = r_adt.relation[ad_key]
                query = "_type:{},{}:{}".format(cmdb_key.get('type_name'), cmdb_key.get('attr_name'),
                                                adc.instance.get(ad_key))
                s = search(query)
                try:
                    response, _, _, _, _, _ = s.search()
                except SearchError as e:
                    current_app.logger.warning(e)
                    return abort(400, str(e))

                relation_ci_id = response and response[0]['_id']
                if relation_ci_id:
                    try:
                        CIRelationManager.add(ci_id, relation_ci_id)
                    except:
                        try:
                            CIRelationManager.add(relation_ci_id, ci_id)
                        except:
                            pass

        adc.update(is_accept=True,
                   accept_by=nickname or current_user.nickname,
                   accept_time=datetime.datetime.now(),
                   ci_id=ci_id)


class AutoDiscoveryHTTPManager(object):
    @staticmethod
    def get_categories(name):
        return (ClOUD_MAP.get(name) or {}).get('categories') or []

    @staticmethod
    def get_attributes(name, category):
        tpt = ((ClOUD_MAP.get(name) or {}).get('map') or {}).get(category)
        if tpt and os.path.exists(os.path.join(PWD, tpt)):
            with open(os.path.join(PWD, tpt)) as f:
                return json.loads(f.read())

        return []


class AutoDiscoverySNMPManager(object):

    @staticmethod
    def get_attributes():
        if os.path.exists(os.path.join(PWD, "templates/net_device.json")):
            with open(os.path.join(PWD, "templates/net_device.json")) as f:
                return json.loads(f.read())

        return []
