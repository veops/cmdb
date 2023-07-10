# -*- coding:utf-8 -*-

class CommonErrFormat(object):
    unauthorized = "未认证"
    unknown_error = "未知错误"

    invalid_request = "不合法的请求"
    invalid_operation = "无效的操作"

    not_found = "不存在"

    unknown_search_error = "未知搜索错误"

    invalid_json = "json格式似乎不正确了, 请仔细确认一下!"

    datetime_argument_invalid = "参数 {} 格式不正确, 格式必须是: yyyy-mm-dd HH:MM:SS"

    argument_value_required = "参数 {} 的值不能为空!"
    argument_required = "请求缺少参数 {}"
    argument_invalid = "参数 {} 的值无效"
    argument_str_length_limit = "参数 {} 的长度必须 <= {}"

    role_required = "角色 {} 才能操作!"
    user_not_found = "用户 {} 不存在"
    no_permission = "您没有资源: {} 的{}权限!"
    no_permission2 = "您没有操作权限!"
    no_permission_only_owner = "只有创建人或者管理员才有权限!"
