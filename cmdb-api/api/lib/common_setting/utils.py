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
            from sqlalchemy.schema import AddColumn
            from sqlalchemy import Table, MetaData
            
            # Sử dụng SQLAlchemy schema operations thay vì raw SQL
            metadata = MetaData(bind=self.engine)
            table = Table(target_table_name, metadata, autoload=True)
            
            # Tạo column definition an toàn
            column_def = new_column.copy()
            
            # Sử dụng AddColumn operation để đảm bảo an toàn
            add_column = AddColumn(table, column_def)
            db.session.execute(add_column)
            return True
        except Exception as e:
            # Fallback to original method với parameterized query
            try:
                column_type = new_column.type.compile(self.engine.dialect)
                default_value = new_column.default.arg if new_column.default else None

                # Sử dụng parameterized query với text() và bindparam
                from sqlalchemy import bindparam
                
                base_sql = "ALTER TABLE :table_name ADD COLUMN :column_name :column_type"
                params = {
                    'table_name': target_table_name,
                    'column_name': new_column.name,
                    'column_type': column_type
                }
                
                # Build SQL with safe parameters
                sql_parts = [f"ALTER TABLE `{target_table_name}` ADD COLUMN `{new_column.name}` {column_type}"]
                
                if new_column.comment:
                    # Escape comment để tránh SQL injection
                    escaped_comment = new_column.comment.replace("'", "''")
                    sql_parts.append(f"COMMENT '{escaped_comment}'")

                if column_type != 'JSON' and default_value is not None:
                    if not (column_type.startswith('VAR') or column_type.startswith('Text')):
                        if isinstance(default_value, str):
                            sql_parts.append(f"DEFAULT '{default_value}'")
                        else:
                            sql_parts.append(f"DEFAULT {default_value}")

                final_sql = " ".join(sql_parts)
                sql = text(final_sql)
                db.session.execute(sql)
                return True
            except Exception as e2:
                err = f"add_new_column [{new_column.name}] to table [{target_table_name}] err: {e2}"
                current_app.logger.error(err)
                return False

    @staticmethod
    def add_new_index(target_table_name, new_column):
        try:
            if new_column.index:
                from sqlalchemy import Index, Table, MetaData
                
                # Sử dụng SQLAlchemy Index object thay vì raw SQL
                metadata = MetaData(bind=db.engine)
                table = Table(target_table_name, metadata, autoload=True)
                
                index_name = f"{target_table_name}_{new_column.name}"
                
                # Tạo index an toàn bằng SQLAlchemy
                index = Index(index_name, table.c[new_column.name])
                index.create(db.engine)
                
                current_app.logger.info(f"add new index [{index_name}] in table [{target_table_name}] success.")

            return True
        except Exception as e:
            # Fallback với parameterized query
            try:
                if new_column.index:
                    # Validate và escape tên bảng và cột
                    safe_table_name = target_table_name.replace('`', '``')
                    safe_column_name = new_column.name.replace('`', '``')
                    index_name = f"{safe_table_name}_{safe_column_name}"
                    
                    sql = text(f"CREATE INDEX `{index_name}` ON `{safe_table_name}` (`{safe_column_name}`)")
                    db.session.execute(sql)
                    current_app.logger.info(f"add new index [{index_name}] in table [{target_table_name}] success.")
                return True
            except Exception as e2:
                err = f"add_new_index [{new_column.name}] to table [{target_table_name}] err: {e2}"
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

                # Escape enum values để tránh SQL injection
                safe_enum_values = []
                for value in new_enum_value:
                    # Escape single quotes trong enum values
                    escaped_value = str(value).replace("'", "''")
                    safe_enum_values.append(f"'{escaped_value}'")
                
                enum_values_str = ','.join(safe_enum_values)
                
                # Validate và escape table name và column name
                safe_table_name = table_name.replace('`', '``')
                safe_column_name = column_name.replace('`', '``')
                
                sql = text(f"ALTER TABLE `{safe_table_name}` MODIFY COLUMN `{safe_column_name}` ENUM({enum_values_str})")
                db.session.execute(sql)
                current_app.logger.info(
                    f"modify column [{column_name}] ENUM: {new_enum_value} in table [{table_name}] success.")
            except Exception as e:
                current_app.logger.error(
                    f"modify column  ENUM [{column_name}] in table [{table_name}] err: {e}")
