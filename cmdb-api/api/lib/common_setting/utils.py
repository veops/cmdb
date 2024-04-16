# -*- coding:utf-8 -*-
from datetime import datetime
from flask import current_app
from sqlalchemy import inspect, text
from sqlalchemy.dialects.mysql import ENUM

from api.extensions import db


def get_cur_time_str(split_flag='-'):
    f = f"%Y{split_flag}%m{split_flag}%d{split_flag}%H{split_flag}%M{split_flag}%S{split_flag}%f"
    return datetime.now().strftime(f)[:-3]


class BaseEnum(object):
    _ALL_ = set()

    @classmethod
    def is_valid(cls, item):
        return item in cls.all()

    @classmethod
    def all(cls):
        if not cls._ALL_:
            cls._ALL_ = {
                getattr(cls, attr)
                for attr in dir(cls)
                if not attr.startswith("_") and not callable(getattr(cls, attr))
            }
        return cls._ALL_


class CheckNewColumn(object):

    def __init__(self):
        self.engine = db.get_engine()
        self.inspector = inspect(self.engine)
        self.table_names = self.inspector.get_table_names()

    @staticmethod
    def get_model_by_table_name(_table_name):
        registry = getattr(db.Model, 'registry', None)
        class_registry = getattr(registry, '_class_registry', None)
        for _model in class_registry.values():
            if hasattr(_model, '__tablename__') and _model.__tablename__ == _table_name:
                return _model
        return None

    def run(self):
        for table_name in self.table_names:
            self.check_by_table(table_name)

    def check_by_table(self, table_name):
        existed_columns = self.inspector.get_columns(table_name)
        enum_columns = []
        existed_column_name_list = []
        for c in existed_columns:
            if isinstance(c['type'], ENUM):
                enum_columns.append(c['name'])
            existed_column_name_list.append(c['name'])

        model = self.get_model_by_table_name(table_name)
        if model is None:
            return
        model_columns = getattr(getattr(getattr(model, '__table__'), 'columns'), '_all_columns')
        for column in model_columns:
            if column.name not in existed_column_name_list:
                add_res = self.add_new_column(table_name, column)
                if not add_res:
                    continue

                current_app.logger.info(f"add new column [{column.name}] in table [{table_name}] success.")

                if column.name in enum_columns:
                    enum_columns.remove(column.name)

                self.add_new_index(table_name, column)

        if len(enum_columns) > 0:
            self.check_enum_column(enum_columns, existed_columns, model_columns, table_name)

    def add_new_column(self, target_table_name, new_column):
        try:
            column_type = new_column.type.compile(self.engine.dialect)
            default_value = new_column.default.arg if new_column.default else None

            sql = "ALTER TABLE " + target_table_name + " ADD COLUMN " + f"`{new_column.name}`" + " " + column_type
            if new_column.comment:
                sql += f" comment '{new_column.comment}'"

            if column_type == 'JSON':
                pass
            elif default_value:
                if column_type.startswith('VAR') or column_type.startswith('Text'):
                    if default_value is None or len(default_value) == 0:
                        pass
                else:
                    sql += f" DEFAULT {default_value}"

            sql = text(sql)
            db.session.execute(sql)
            return True
        except Exception as e:
            err = f"add_new_column [{new_column.name}] to table [{target_table_name}] err: {e}"
            current_app.logger.error(err)
            return False

    @staticmethod
    def add_new_index(target_table_name, new_column):
        try:
            if new_column.index:
                index_name = f"{target_table_name}_{new_column.name}"
                sql = "CREATE INDEX " + f"{index_name}" + " ON " + target_table_name + " (" + new_column.name + ")"
                db.session.execute(sql)
                current_app.logger.info(f"add new index [{index_name}] in table [{target_table_name}] success.")

            return True
        except Exception as e:
            err = f"add_new_index [{new_column.name}] to table [{target_table_name}] err: {e}"
            current_app.logger.error(err)
            return False

    @staticmethod
    def check_enum_column(enum_columns, existed_columns, model_columns, table_name):
        for column_name in enum_columns:
            try:
                enum_column = list(filter(lambda x: x['name'] == column_name, existed_columns))[0]
                old_enum_value = enum_column.get('type', {}).enums
                target_column = list(filter(lambda x: x.name == column_name, model_columns))[0]
                new_enum_value = target_column.type.enums

                if set(old_enum_value) == set(new_enum_value):
                    continue

                enum_values_str = ','.join(["'{}'".format(value) for value in new_enum_value])
                sql = f"ALTER TABLE {table_name} MODIFY COLUMN" + f"`{column_name}`" + f" enum({enum_values_str})"
                db.session.execute(sql)
                current_app.logger.info(
                    f"modify column [{column_name}] ENUM: {new_enum_value} in table [{table_name}] success.")
            except Exception as e:
                current_app.logger.error(
                    f"modify column  ENUM [{column_name}] in table [{table_name}] err: {e}")
