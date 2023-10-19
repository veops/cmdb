# -*- coding:utf-8 -*-


from functools import wraps

from flask import abort
from flask import current_app
from flask import request
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import StatementError

from api.extensions import db
from api.lib.resp_format import CommonErrFormat


def kwargs_required(*required_args):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in required_args:
                if arg not in kwargs:
                    return abort(400, CommonErrFormat.argument_required.format(arg))

            return func(*args, **kwargs)

        return wrapper

    return decorate


def args_required(*required_args, **value_required):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in required_args:
                if arg not in request.values:
                    return abort(400, CommonErrFormat.argument_required.format(arg))

                if value_required.get('value_required', True) and not request.values.get(arg):
                    return abort(400, CommonErrFormat.argument_value_required.format(arg))

            return func(*args, **kwargs)

        return wrapper

    return decorate


def args_validate(model_cls, exclude_args=None):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in request.values:
                if hasattr(model_cls, arg):
                    attr = getattr(model_cls, arg)
                    if not hasattr(attr, "type"):
                        continue

                    if exclude_args and arg in exclude_args:
                        continue

                    if attr.type.python_type == str and attr.type.length and (
                            len(request.values[arg] or '') > attr.type.length):

                        return abort(400, CommonErrFormat.argument_str_length_limit.format(arg, attr.type.length))
                    elif attr.type.python_type in (int, float) and request.values[arg]:
                        try:
                            int(float(request.values[arg]))
                        except (TypeError, ValueError):
                            return abort(400, CommonErrFormat.argument_invalid.format(arg))

            return func(*args, **kwargs)

        return wrapper

    return decorate


def reconnect_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (StatementError, OperationalError, InvalidRequestError) as e:
            error_msg = str(e)
            if 'Lost connection' in error_msg or 'reconnect until invalid transaction' in error_msg or \
                    'can be emitted within this transaction' in error_msg:
                current_app.logger.info('[reconnect_db] lost connect rollback then retry')
                db.session.rollback()
                return func(*args, **kwargs)
            else:
                raise e
        except Exception as e:
            raise e

    return wrapper


def _flush_db():
    db.session.commit()


def flush_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _flush_db()
        return func(*args, **kwargs)

    return wrapper


def run_flush_db():
    _flush_db()
