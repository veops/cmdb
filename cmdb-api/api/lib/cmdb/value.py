# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

import copy
import imp
import os
import tempfile

import jinja2
from flask import abort
from flask import current_app
from jinja2schema import infer
from jinja2schema import to_json_schema

from api.extensions import db
from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributeCache
from api.lib.cmdb.const import OperateType
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.cmdb.history import AttributeHistoryManger
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.utils import TableMap
from api.lib.cmdb.utils import ValueTypeMap
from api.lib.utils import handle_arg_list
from api.models.cmdb import CI


class AttributeValueManager(object):
    """
    manage CI attribute values
    """

    def __init__(self):
        pass

    @staticmethod
    def _get_attr(key):
        """
        :param key: id, name or alias
        :return: attribute instance
        """
        return AttributeCache.get(key)

    def get_attr_values(self, fields, ci_id, ret_key="name", unique_key=None, use_master=False):
        """

        :param fields:
        :param ci_id:
        :param ret_key: It can be name or alias
        :param unique_key: primary attribute
        :param use_master: Only for master-slave read-write separation
        :return:
        """
        res = dict()
        for field in fields:
            attr = self._get_attr(field)
            if not attr:
                continue

            value_table = TableMap(attr=attr).table
            rs = value_table.get_by(ci_id=ci_id,
                                    attr_id=attr.id,
                                    use_master=use_master,
                                    to_dict=False)
            field_name = getattr(attr, ret_key)
            if attr.is_list:
                res[field_name] = [ValueTypeMap.serialize[attr.value_type](i.value) for i in rs]
            elif attr.is_password and rs:
                res[field_name] = '******' if rs[0].value else ''
            else:
                res[field_name] = ValueTypeMap.serialize[attr.value_type](rs[0].value) if rs else None

            if unique_key is not None and attr.id == unique_key.id and rs:
                res['unique'] = unique_key.name
                res['unique_alias'] = unique_key.alias

        return res

    @staticmethod
    def _deserialize_value(value_type, value):
        if not value:
            return value

        deserialize = ValueTypeMap.deserialize[value_type]
        try:
            v = deserialize(value)
            return v
        except ValueError:
            return abort(400, ErrFormat.attribute_value_invalid.format(value))

    @staticmethod
    def _check_is_choice(attr, value_type, value):
        choice_values = AttributeManager.get_choice_values(attr.id, value_type, attr.choice_web_hook, attr.choice_other)
        if value_type == ValueTypeEnum.FLOAT:
            if float(value) not in list(map(float, [i[0] for i in choice_values])):
                return abort(400, ErrFormat.not_in_choice_values.format(value))

        else:
            if str(value) not in list(map(str, [i[0] for i in choice_values])):
                return abort(400, ErrFormat.not_in_choice_values.format(value))

    @staticmethod
    def _check_is_unique(value_table, attr, ci_id, type_id, value):
        existed = db.session.query(value_table.attr_id).join(CI, CI.id == value_table.ci_id).filter(
            CI.type_id == type_id).filter(
            value_table.attr_id == attr.id).filter(value_table.deleted.is_(False)).filter(
            value_table.value == value).filter(value_table.ci_id != ci_id).first()

        existed and abort(400, ErrFormat.attribute_value_unique_required.format(attr.alias, value))

    @staticmethod
    def _check_is_required(type_id, attr, value, type_attr=None):
        type_attr = type_attr or CITypeAttributeCache.get(type_id, attr.id)
        if type_attr and type_attr.is_required and not value and value != 0:
            return abort(400, ErrFormat.attribute_value_required.format(attr.alias))

    def _validate(self, attr, value, value_table, ci=None, type_id=None, ci_id=None, type_attr=None):
        ci = ci or {}
        v = self._deserialize_value(attr.value_type, value)

        attr.is_choice and value and self._check_is_choice(attr, attr.value_type, v)
        attr.is_unique and self._check_is_unique(
            value_table, attr, ci and ci.id or ci_id, ci and ci.type_id or type_id, v)

        self._check_is_required(ci and ci.type_id or type_id, attr, v, type_attr=type_attr)

        if v == "" and attr.value_type not in (ValueTypeEnum.TEXT,):
            v = None

        return v

    @staticmethod
    def _write_change(ci_id, attr_id, operate_type, old, new, record_id, type_id):
        return AttributeHistoryManger.add(record_id, ci_id, [(attr_id, operate_type, old, new)], type_id)

    @staticmethod
    def write_change2(changed, record_id=None):
        for ci_id, attr_id, operate_type, old, new, type_id in changed:
            record_id = AttributeHistoryManger.add(record_id, ci_id, [(attr_id, operate_type, old, new)], type_id,
                                                   commit=False, flush=False)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("write change failed: {}".format(str(e)))

        return record_id

    @staticmethod
    def _compute_attr_value_from_expr(expr, ci_dict):
        t = jinja2.Template(expr).render(ci_dict)

        try:
            return eval(t)
        except Exception as e:
            current_app.logger.warning(str(e))
            return t

    @staticmethod
    def _compute_attr_value_from_script(script, ci_dict):
        script = jinja2.Template(script).render(ci_dict)

        script_f = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
        script_f.write(script.encode('utf-8'))
        script_f.close()

        try:
            path = script_f.name
            dir_name, name = os.path.dirname(path), os.path.basename(path)[:-3]

            fp, path, desc = imp.find_module(name, [dir_name])

            mod = imp.load_module(name, fp, path, desc)

            if hasattr(mod, 'computed'):
                return mod.computed()
        except Exception as e:
            current_app.logger.error(str(e))

        finally:
            os.remove(script_f.name)

    @staticmethod
    def _jinja2_parse(content):
        schema = to_json_schema(infer(content))

        return [var for var in schema.get("properties")]

    def _compute_attr_value(self, attr, payload, ci_id):
        attrs = (self._jinja2_parse(attr['compute_expr']) if attr.get('compute_expr')
                 else self._jinja2_parse(attr['compute_script']))
        not_existed = [i for i in attrs if i not in payload]
        if ci_id is not None:
            payload.update(self.get_attr_values(not_existed, ci_id))

        if attr['compute_expr']:
            return self._compute_attr_value_from_expr(attr['compute_expr'], payload)
        elif attr['compute_script']:
            return self._compute_attr_value_from_script(attr['compute_script'], payload)

    def handle_ci_compute_attributes(self, ci_dict, computed_attrs, ci):
        payload = copy.deepcopy(ci_dict)
        for attr in computed_attrs:
            computed_value = self._compute_attr_value(attr, payload, ci and ci.id)
            if computed_value is not None:
                ci_dict[attr['name']] = computed_value

    def valid_attr_value(self, ci_dict, type_id, ci_id, name2attr, alias2attr=None, ci_attr2type_attr=None):
        key2attr = dict()
        alias2attr = alias2attr or {}
        ci_attr2type_attr = ci_attr2type_attr or {}

        for key, value in ci_dict.items():
            attr = name2attr.get(key) or alias2attr.get(key)
            key2attr[key] = attr

            value_table = TableMap(attr=attr).table

            try:
                if attr.is_list:
                    value_list = [self._validate(attr, i, value_table, ci=None, type_id=type_id, ci_id=ci_id,
                                                 type_attr=ci_attr2type_attr.get(attr.id))
                                  for i in handle_arg_list(value)]
                    ci_dict[key] = value_list
                    if not value_list:
                        self._check_is_required(type_id, attr, '')

                else:
                    value = self._validate(attr, value, value_table, ci=None, type_id=type_id, ci_id=ci_id,
                                           type_attr=ci_attr2type_attr.get(attr.id))
                    ci_dict[key] = value
            except Exception as e:
                current_app.logger.warning(str(e))

                return abort(400, ErrFormat.attribute_value_invalid2.format(
                    "{}({})".format(attr.alias, attr.name), value))

        return key2attr

    def create_or_update_attr_value(self, ci, ci_dict, key2attr):
        """
        add or update attribute value, then write history
        :param ci: instance object
        :param ci_dict: attribute dict
        :param key2attr: attr key to attr
        :return:
        """
        changed = []
        for key, value in ci_dict.items():
            attr = key2attr.get(key)
            if not attr:
                continue  # not be here
            value_table = TableMap(attr=attr).table

            if attr.is_list:
                existed_attrs = value_table.get_by(attr_id=attr.id, ci_id=ci.id, to_dict=False)
                existed_values = [i.value for i in existed_attrs]
                added = set(value) - set(existed_values)
                deleted = set(existed_values) - set(value)
                for v in added:
                    value_table.create(ci_id=ci.id, attr_id=attr.id, value=v, flush=False, commit=False)
                    changed.append((ci.id, attr.id, OperateType.ADD, None, v, ci.type_id))

                for v in deleted:
                    existed_attr = existed_attrs[existed_values.index(v)]
                    existed_attr.delete(flush=False, commit=False)
                    changed.append((ci.id, attr.id, OperateType.DELETE, v, None, ci.type_id))
            else:
                existed_attr = value_table.get_by(attr_id=attr.id, ci_id=ci.id, first=True, to_dict=False)
                existed_value = existed_attr and existed_attr.value
                if existed_value is None and value is not None:
                    value_table.create(ci_id=ci.id, attr_id=attr.id, value=value, flush=False, commit=False)

                    changed.append((ci.id, attr.id, OperateType.ADD, None, value, ci.type_id))
                else:
                    if existed_value != value:
                        if value is None:
                            existed_attr.delete(flush=False, commit=False)
                        else:
                            existed_attr.update(value=value, flush=False, commit=False)

                        changed.append((ci.id, attr.id, OperateType.UPDATE, existed_value, value, ci.type_id))

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.warning(str(e))
            return abort(400, ErrFormat.attribute_value_unknown_error.format(e.args[0]))

        return self.write_change2(changed)

    @staticmethod
    def delete_attr_value(attr_id, ci_id):
        attr = AttributeCache.get(attr_id)
        if attr is not None:
            value_table = TableMap(attr=attr).table
            for item in value_table.get_by(attr_id=attr.id, ci_id=ci_id, to_dict=False):
                item.delete()
