# -*- coding:utf-8 -*-

from api.lib.resp_format import CommonErrFormat


class ErrFormat(CommonErrFormat):
    login_succeed = "登录成功"
    ldap_connection_failed = "连接LDAP服务失败"
    invalid_password = "密码验证失败"
    auth_only_with_app_token_failed = "应用 Token验证失败"
    session_invalid = "您不是应用管理员 或者 session失效(尝试一下退出重新登录)"

    resource_type_not_found = "资源类型 {} 不存在!"
    resource_type_exists = "资源类型 {} 已经存在!"
    resource_type_cannot_delete = "因为该类型下有资源的存在, 不能删除!"

    user_not_found = "用户 {} 不存在!"
    user_exists = "用户 {} 已经存在!"
    role_not_found = "角色 {} 不存在!"
    role_exists = "角色 {} 已经存在!"
    global_role_not_found = "全局角色 {} 不存在!"
    global_role_exists = "全局角色 {} 已经存在!"

    resource_no_permission = "您没有资源: {} 的 {} 权限"
    admin_required = "需要管理员权限"
    role_required = "需要角色: {}"
    user_role_delete_invalid = "删除用户角色, 请在 用户管理 页面操作!"

    app_is_ready_existed = "应用 {} 已经存在"
    app_not_found = "应用 {} 不存在!"
    app_secret_invalid = "应用的Secret无效"

    resource_not_found = "资源 {} 不存在!"
    resource_exists = "资源 {} 已经存在!"

    resource_group_not_found = "资源组 {} 不存在!"
    resource_group_exists = "资源组 {} 已经存在!"

    inheritance_dead_loop = "继承检测到了死循环"
    role_relation_not_found = "角色关系 {} 不存在!"

    trigger_not_found = "触发器 {} 不存在!"
    trigger_exists = "触发器 {} 已经存在!"
    trigger_disabled = "触发器 {} 已经被禁用!"

    invalid_password = "密码不正确!"
