# -*- coding:utf-8 -*- 


from flask import abort
from flask import g

from api.extensions import db
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import RelationTypeCache
from api.lib.perm.acl.cache import UserCache
from api.models.cmdb import Attribute
from api.models.cmdb import AttributeHistory
from api.models.cmdb import CIRelationHistory
from api.models.cmdb import OperationRecord


class AttributeHistoryManger(object):
    @staticmethod
    def get_records(start, end, username, page, page_size):
        records = db.session.query(OperationRecord).filter(OperationRecord.deleted.is_(False))
        numfound = db.session.query(db.func.count(OperationRecord.id)).filter(OperationRecord.deleted.is_(False))
        if start:
            records = records.filter(OperationRecord.created_at >= start)
            numfound = numfound.filter(OperationRecord.created_at >= start)
        if end:
            records = records.filter(OperationRecord.created_at <= end)
            numfound = records.filter(OperationRecord.created_at <= end)
        if username:
            user = UserCache.get(username)
            if user:
                records = records.filter(OperationRecord.uid == user.uid)
            else:
                return abort(404, "User <{0}> is not found".format(username))

        records = records.order_by(-OperationRecord.id).offset(page_size * (page - 1)).limit(page_size).all()
        total = len(records)
        numfound = numfound.first()[0]
        res = []
        for record in records:
            _res = record.to_dict()
            _res["user"] = UserCache.get(_res.get("uid")).nickname or UserCache.get(_res.get("uid")).username

            attr_history = AttributeHistory.get_by(record_id=_res.get("id"), to_dict=False)
            _res["attr_history"] = [AttributeCache.get(h.attr_id).attr_alias for h in attr_history]

            rel_history = CIRelationHistory.get_by(record_id=_res.get("id"), to_dict=False)
            rel_statis = {}
            for rel in rel_history:
                if rel.operate_type not in rel_statis:
                    rel_statis[rel.operate_type] = 1
                else:
                    rel_statis[rel.operate_type] += 1
            _res["rel_history"] = rel_statis
            res.append(_res)

        return numfound, total, res

    @staticmethod
    def get_by_ci_id(ci_id):
        res = db.session.query(AttributeHistory, Attribute, OperationRecord).join(
            Attribute, Attribute.id == AttributeHistory.attr_id).join(
            OperationRecord, OperationRecord.id == AttributeHistory.record_id).filter(
            AttributeHistory.ci_id == ci_id).order_by(OperationRecord.id.desc())
        return [dict(attr_name=i.Attribute.name,
                     attr_alias=i.Attribute.alias,
                     operate_type=i.AttributeHistory.operate_type,
                     username=UserCache.get(i.OperationRecord.uid).nickname,
                     old=i.AttributeHistory.old,
                     new=i.AttributeHistory.new,
                     created_at=i.OperationRecord.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                     record_id=i.OperationRecord.id,
                     hid=i.AttributeHistory.id
                     ) for i in res]

    @staticmethod
    def get_record_detail(record_id):
        from api.lib.cmdb.ci import CIManager

        record = OperationRecord.get_by_id(record_id) or abort(404, "Record <{0}> is not found".format(record_id))

        username = UserCache.get(record.uid).nickname or UserCache.get(record.uid).username
        timestamp = record.created_at.strftime("%Y-%m-%d %H:%M:%S")
        attr_history = AttributeHistory.get_By(record_id=record_id, to_dict=False)
        rel_history = CIRelationHistory.get_by(record_id=record_id, to_dict=False)

        attr_dict, rel_dict = dict(), {"add": [], "delete": []}
        for attr_h in attr_history:
            attr_dict[AttributeCache.get(attr_h.attr_id).alias] = dict(
                old=attr_h.old,
                new=attr_h.new,
                operate_type=attr_h.operate_type)

        for rel_h in rel_history:
            first = CIManager.get_ci_by_id(rel_h.first_ci_id)
            second = CIManager.get_ci_by_id(rel_h.second_ci_id)
            rel_dict[rel_h.operate_type].append((first, RelationTypeCache.get(rel_h.relation_type_id).name, second))

        return username, timestamp, attr_dict, rel_dict

    @staticmethod
    def add(ci_id, history_list):
        record = OperationRecord.create(uid=g.user.uid)

        for attr_id, operate_type, old, new in history_list or []:
            AttributeHistory.create(attr_id=attr_id,
                                    operate_type=operate_type,
                                    old=old,
                                    new=new,
                                    ci_id=ci_id,
                                    record_id=record.id)


class CIRelationHistoryManager(object):
    @staticmethod
    def add(rel_obj, operate_type=CIRelationHistory.ADD):
        record = OperationRecord.create(uid=g.user.uid)

        CIRelationHistory.create(relation_id=rel_obj.id,
                                 record_id=record.id,
                                 operate_type=operate_type,
                                 first_ci_id=rel_obj.first_ci_id,
                                 second_ci_id=rel_obj.second_ci_id,
                                 relation_type_id=rel_obj.relation_type_id)
