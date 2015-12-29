# -*- coding:utf-8 -*- 


import datetime

from flask import current_app
from flask import g

from extensions import db
from models.history import OperationRecord
from models.history import CIAttributeHistory
from models.history import CIRelationHistory


class CIAttributeHistoryManger(object):
    def __init__(self):
        pass

    def add(self, ci_id, history_list):
        if history_list:
            record = OperationRecord()
            record.uid = g.user.uid
            record.timestamp = datetime.datetime.now()
            db.session.add(record)
            db.session.commit()
            for attr_id, operate_type, old, new in history_list:
                history = CIAttributeHistory()
                history.attr_id = attr_id
                history.operate_type = operate_type
                history.old = old
                history.new = new
                history.ci_id = ci_id
                history.record_id = record.record_id
                db.session.add(history)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                db.session.rollback()
                current_app.logger.error(
                    "add attribute history error, {0}".format(str(e)))
                return False, "add attribute history error, {0}".format(str(e))
        return True, None


class CIRelationHistoryManager(object):
    def __init__(self):
        pass

    def add(self, relation, first_ci, second_ci,
            relation_type, operate_type="add"):
        record = OperationRecord()
        record.uid = g.user.uid
        record.timestamp = datetime.datetime.now()
        db.session.add(record)
        db.session.flush()

        history = CIRelationHistory()
        history.relation = relation
        history.record_id = record.record_id
        history.operate_type = operate_type
        history.first_ci_id = first_ci
        history.second_ci_id = second_ci
        history.relation_type = relation_type
        db.session.add(history)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                "add relation history is error, {0}".format(str(e)))
            return False, "add relation history is error, {0}".format(str(e))
        return True, None
