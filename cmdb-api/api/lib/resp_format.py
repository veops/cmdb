# -*- coding:utf-8 -*-

from flask_babel import lazy_gettext as _l


class CommonErrFormat(object):
    unauthorized = _l("unauthorized")  # 未认证
    unknown_error = _l("unknown error")  # 未知错误

    invalid_request = _l("Illegal request")  # 不合法的请求
    invalid_operation = _l("Invalid operation")  # 无效的操作

    not_found = _l("does not exist")  # 不存在

    circular_dependency_error = _l("There is a circular dependency!")  # 存在循环依赖!

    unknown_search_error = _l("Unknown search error")  # 未知搜索错误

    # json格式似乎不正确了, 请仔细确认一下!
    invalid_json = _l("The json format seems to be incorrect, please confirm carefully!")

    # 参数 {} 格式不正确, 格式必须是: yyyy-mm-dd HH:MM:SS
    datetime_argument_invalid = _l("The format of parameter {} is incorrect, the format must be: yyyy-mm-dd HH:MM:SS")

    argument_value_required = _l("The value of parameter {} cannot be empty!")  # 参数 {} 的值不能为空!
    argument_required = _l("The request is missing parameters {}")  # 请求缺少参数 {}
    argument_invalid = _l("Invalid value for parameter {}")  # 参数 {} 的值无效
    argument_str_length_limit = _l("The length of parameter {} must be <= {}")  # 参数 {} 的长度必须 <= {}

    role_required = _l("Role {} can only operate!")  # 角色 {} 才能操作!
    user_not_found = _l("User {} does not exist")  # 用户 {} 不存在
    no_permission = _l("You do not have {} permission for resource: {}!")  # 您没有资源: {} 的{}权限!
    no_permission2 = _l("You do not have permission to operate!")  # 您没有操作权限!
    no_permission_only_owner = _l("Only the creator or administrator has permission!")  # 只有创建人或者管理员才有权限!
