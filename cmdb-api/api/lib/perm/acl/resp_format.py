# -*- coding:utf-8 -*-

from flask_babel import lazy_gettext as _l

from api.lib.resp_format import CommonErrFormat


class ErrFormat(CommonErrFormat):
    login_succeed = _l("login successful")  # 登录成功
    ldap_connection_failed = _l("Failed to connect to LDAP service")  # 连接LDAP服务失败
    invalid_password = _l("Password verification failed")  # 密码验证失败
    auth_only_with_app_token_failed = _l("Application Token verification failed")  # 应用 Token验证失败
    # 您不是应用管理员 或者 session失效(尝试一下退出重新登录)
    session_invalid = _l(
        "You are not the application administrator or the session has expired (try logging out and logging in again)")

    resource_type_not_found = _l("Resource type {} does not exist!")  # 资源类型 {} 不存在!
    resource_type_exists = _l("Resource type {} already exists!")  # 资源类型 {} 已经存在!
    # 因为该类型下有资源的存在, 不能删除!
    resource_type_cannot_delete = _l("Because there are resources under this type, they cannot be deleted!")

    user_not_found = _l("User {} does not exist!")  # 用户 {} 不存在!
    user_exists = _l("User {} already exists!")  # 用户 {} 已经存在!
    role_not_found = _l("Role {} does not exist!")  # 角色 {} 不存在!
    role_exists = _l("Role {} already exists!")  # 角色 {} 已经存在!
    global_role_not_found = _l("Global role {} does not exist!")  # 全局角色 {} 不存在!
    global_role_exists = _l("Global role {} already exists!")  # 全局角色 {} 已经存在!

    resource_no_permission = _l("You do not have {} permission on resource: {}")  # 您没有资源: {} 的 {} 权限
    admin_required = _l("Requires administrator permissions")  # 需要管理员权限
    role_required = _l("Requires role: {}")  # 需要角色: {}
    # 删除用户角色, 请在 用户管理 页面操作!
    user_role_delete_invalid = _l("To delete a user role, please operate on the User Management page!")

    app_is_ready_existed = _l("Application {} already exists")  # 应用 {} 已经存在
    app_not_found = _l("Application {} does not exist!")  # 应用 {} 不存在!
    app_secret_invalid = _l("The Secret is invalid")  # 应用的Secret无效

    resource_not_found = _l("Resource {} does not exist!")  # 资源 {} 不存在!
    resource_exists = _l("Resource {} already exists!")  # 资源 {} 已经存在!

    resource_group_not_found = _l("Resource group {} does not exist!")  # 资源组 {} 不存在!
    resource_group_exists = _l("Resource group {} already exists!")  # 资源组 {} 已经存在!

    inheritance_dead_loop = _l("Inheritance detected infinite loop")  # 继承检测到了死循环
    role_relation_not_found = _l("Role relationship {} does not exist!")  # 角色关系 {} 不存在!

    trigger_not_found = _l("Trigger {} does not exist!")  # 触发器 {} 不存在!
    trigger_exists = _l("Trigger {} already exists!")  # 触发器 {} 已经存在!
    trigger_disabled = _l("Trigger {} has been disabled!")  # Trigger {} has been disabled!
