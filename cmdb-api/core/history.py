# -*- coding:utf-8 -*- 


import datetime

from flask import jsonify
from flask import current_app
from flask import Blueprint
from flask import request
from flask import abort

from models.history import OperationRecord
from models.history import CIRelationHistory
from models.history import CIAttributeHistory
from models.attribute import CIAttributeCache
from extensions import db
from models import row2dict
from models.account import UserCache
from lib.ci import CIManager
from lib.utils import get_page

history = Blueprint("history", __name__)


@history.route("/record", methods=["GET"])
def get_record():
    page = get_page(request.values.get("page", 1))
    _start = request.values.get("start")
    _end = request.values.get("end")
    username = request.values.get("username", "")
    per_page_cnt = current_app.config.get("DEFAULT_PAGE_COUNT")
    start, end = None, None
    if _start:
        try:
            start = datetime.datetime.strptime(_start, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            abort(400, 'incorrect start date time')
    if _end:
        try:
            end = datetime.datetime.strptime(_end, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            abort(400, 'incorrect end date time')
    records = db.session.query(OperationRecord)
    numfound = db.session.query(db.func.count(OperationRecord.record_id))
    if start:
        records = records.filter(OperationRecord.timestamp >= start)
        numfound = numfound.filter(OperationRecord.timestamp >= start)
    if end:
        records = records.filter(OperationRecord.timestamp <= end)
        numfound = records.filter(OperationRecord.timestamp <= end)
    if username:
        user = UserCache.get(username)
        if user:
            records = records.filter(OperationRecord.uid == user.uid)
        else:
            return jsonify(numfound=0, records=[],
                           page=1, total=0, start=_start,
                           end=_end, username=username)
    records = records.order_by(-OperationRecord.record_id).offset(
        per_page_cnt * (page - 1)).limit(per_page_cnt).all()
    total = len(records)
    numfound = numfound.first()[0]
    res = []
    for record in records:
        _res = row2dict(record)
        _res["user"] = UserCache.get(_res.get("uid")).nickname \
            if UserCache.get(_res.get("uid")).nickname \
            else UserCache.get(_res.get("uid")).username
        attr_history = db.session.query(CIAttributeHistory.attr_id).filter(
            CIAttributeHistory.record_id == _res.get("record_id")).all()
        _res["attr_history"] = [CIAttributeCache.get(h.attr_id).attr_alias
                                for h in attr_history]
        rel_history = db.session.query(CIRelationHistory.operate_type).filter(
            CIRelationHistory.record_id == _res.get("record_id")).all()
        rel_statis = {}
        for rel in rel_history:
            if rel.operate_type not in rel_statis:
                rel_statis[rel.operate_type] = 1
            else:
                rel_statis[rel.res.operate_type] += 1
        _res["rel_history"] = rel_statis
        res.append(_res)

    return jsonify(numfound=numfound, records=res, page=page, total=total,
                   start=_start, end=_end, username=username)


@history.route("/<int:record_id>", methods=["GET"])
def get_detail_by_record(record_id=None):
    record = db.session.query(OperationRecord).filter(
        OperationRecord.record_id == record_id).first()
    if record is None:
        abort(404, "record is not found")
    username = UserCache.get(record.uid).nickname \
        if UserCache.get(record.uid).nickname \
        else UserCache.get(record.uid).username
    timestamp = record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    attr_history = db.session.query(CIAttributeHistory).filter(
        CIAttributeHistory.record_id == record_id).all()
    rel_history = db.session.query(CIRelationHistory).filter(
        CIRelationHistory.record_id == record_id).all()
    attr_dict, rel_dict = dict(), {"add": [], "delete": []}
    for attr_h in attr_history:
        attr_dict[CIAttributeCache.get(attr_h.attr_id).attr_alias] = {
            "old": attr_h.old, "new": attr_h.new,
            "operate_type": attr_h.operate_type}
    manager = CIManager()
    for rel_h in rel_history:
        _, first = manager.get_ci_by_id(rel_h.first_ci_id)
        _, second = manager.get_ci_by_id(rel_h.second_ci_id)
        rel_dict[rel_h.operate_type].append(
            (first, rel_h.relation_type, second))

    return jsonify(username=username, timestamp=timestamp,
                   attr_history=attr_dict,
                   rel_history=rel_dict)
