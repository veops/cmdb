# -*- coding:utf-8 -*- 

__author__ = 'pycook'

import datetime

from flask import current_app

from models.cmdb import CIAudit
from models.cmdb import CIAttributeAudit
from models.cmdb import CIAttributeCache
from models.cmdb import CITypeCache
from models.cmdb import CI
from models import row2dict
from extensions import db
from lib.const import TableMap
from tasks.cmdb import ci_cache


class CIAuditManager(object):
    def __init__(self):
        pass

    def get_cis_for_audits(self, page, type_ids, per_page=25):
        audit_cis = db.session.query(CIAudit)
        if type_ids:
            audit_cis = audit_cis.join(CI, CI.ci_id == CIAudit.ci_id).filter(
                CI.type_id.in_(type_ids))

        audit_cis = audit_cis.filter(CIAudit.is_audit == 0).order_by(
            CIAudit.created_at)
        numfound = audit_cis.count()
        audit_cis = audit_cis.offset((page - 1) * per_page).limit(per_page)
        total = audit_cis.count()
        audit_cis = audit_cis.all()
        result = list()
        for audit_ci in audit_cis:
            audit_dict = row2dict(audit_ci)
            audit_attrs = db.session.query(CIAttributeAudit).filter(
                CIAttributeAudit.audit_id == audit_ci.audit_id).all()
            audit_dict["values"] = list()
            for audit_attr in audit_attrs:
                audit_attr_dict = row2dict(audit_attr)
                audit_attr_dict["attr_name"] = CIAttributeCache.get(
                    audit_attr.attr_id).attr_name
                audit_dict['values'].append(audit_attr_dict)
            result.append(audit_dict)
        return numfound, total, result

    def create_ci_audits(self, type_name, attr_pairs):
        ci_type = CITypeCache.get(type_name)
        uniq_key = CIAttributeCache.get(ci_type.uniq_id)
        table = TableMap(attr_name=uniq_key.attr_name).table
        value = db.session.query(table.ci_id).filter(
            table.attr_id == uniq_key.attr_id).filter(
                table.value == attr_pairs.get(uniq_key.attr_name)).first()
        del attr_pairs[uniq_key.attr_name]
        if value and attr_pairs:
            ci_audit = db.session.query(CIAudit).filter(
                CIAudit.ci_id == value.ci_id).filter(
                    CIAudit.is_audit == 0).first()
            if ci_audit is None:
                ci_audit = CIAudit()
                ci_audit.is_notified = False
                ci_audit.created_at = datetime.datetime.now()
            ci_audit.ci_id = value.ci_id
            ci_audit.updated_at = datetime.datetime.now()
            ci_audit.origin = 1   # TODO
            db.session.add(ci_audit)
            db.session.commit()
            for attr, attr_value in attr_pairs.items():
                attr_id = CIAttributeCache.get(attr).attr_id
                ci_attr_audit = CIAttributeAudit()
                ci_attr_audit.attr_id = attr_id
                all_values = attr_value.strip().split("###")
                ci_attr_audit.cur_value = all_values[0]
                ci_attr_audit.new_value = all_values[1]
                ci_attr_audit.audit_id = ci_audit.audit_id
                db.session.add(ci_attr_audit)
                db.session.flush()
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error("create ci audits error, %s" % str(e))
                return False, "create ci audits error, %s" % str(e)
        return True, None

    def _update_cmdb(self, ci_id, attr_id, value):
        try:
            attr_name = CIAttributeCache.get(attr_id).attr_name
            table = TableMap(attr_name=attr_name).table
            attr_value = db.session.query(table).filter(
                table.attr_id == attr_id).filter(
                    table.ci_id == ci_id).first()
            attr_value.value = value
            db.session.add(attr_value)

        except Exception as e:
            return False, "audit failed, %s" % str(e)
        return True, ci_id

    def audit_by_attr(self, audit_id, attr_ids, value=None):
        ci_audit = CIAudit.query.get(audit_id)
        ci_id = ci_audit.ci_id
        for attr_id in attr_ids:
            attr_audit = db.session.query(CIAttributeAudit).filter(
                CIAttributeAudit.audit_id == audit_id).filter(
                    CIAttributeAudit.attr_id == attr_id).first()
            if attr_audit:
                attr_audit.is_audit = True
                attr_audit.auditor = 1  # TODO
                attr_audit.audited_at = datetime.datetime.now()
                if value is not None:
                    attr_audit.audit_value = value
                else:
                    attr_audit.audit_value = attr_audit.new_value
                if attr_audit.cur_value != value:  # update cmdb
                    ret, res = self._update_cmdb(ci_id, attr_id, value)
                    if not ret:
                        return False, res
                    attr_audit.is_updated = True
                db.session.add(attr_audit)
                db.session.flush()
            if db.session.query(CIAttributeAudit).filter_by(
                    audit_id=audit_id).filter_by(is_audit=0).first() is None:
                ci_audit.is_audit = True
                ci_audit.updated_at = datetime.datetime.now()
                db.session.add(ci_audit)
        ci_cache.apply_async([ci_id], queue="cmdb_async")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                "audit by attribute is error, {0}".format(str(e)))
            return False, "audit by attribute is error, %s" % str(e)
        return True, None

    def audit_by_cis(self, ci_ids):
        for ci_id in ci_ids:
            ci_audit = db.session.query(CIAudit).filter_by(ci_id=ci_id).first()
            attr_audits = db.session.query(CIAttributeAudit).filter_by(
                audit_id=ci_audit.audit_id).all()
            for attr_audit in attr_audits:
                attr_audit.is_audit = True
                attr_audit.auditor = 1  # TODO
                attr_audit.audited_at = datetime.datetime.now()
                attr_audit.audit_value = attr_audit.new_value
                ret, res = self._update_cmdb(
                    ci_id, attr_audit.attr_id,
                    attr_audit.new_value)
                if not ret:
                    return False, res
                attr_audit.is_updated = True
                db.session.add(attr_audit)
            ci_audit.is_audit = True
            ci_audit.updated_at = datetime.datetime.now()
            db.session.add(ci_audit)
            ci_cache.apply_async([ci_id], queue="cmdb_async")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                "audit by attribute error, {0}".format(str(e)))
            return False, "audit by cis is error, %s" % str(e)
        return True, None
