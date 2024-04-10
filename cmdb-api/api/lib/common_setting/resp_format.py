# -*- coding:utf-8 -*-
from flask_babel import lazy_gettext as _l

from api.lib.resp_format import CommonErrFormat


class ErrFormat(CommonErrFormat):
    company_info_is_already_existed = _l("Company info already existed")  # 公司信息已存在！无法创建

    no_file_part = _l("No file part")  # 没有文件部分
    file_is_required = _l("File is required")  # 文件是必须的
    file_not_found = _l("File not found")  # 文件不存在
    file_type_not_allowed = _l("File type not allowed")  # 文件类型不允许
    upload_failed = _l("Upload failed: {}")  # 上传失败: {}

    direct_supervisor_is_not_self = _l("Direct supervisor is not self")  # 直属上级不能是自己
    parent_department_is_not_self = _l("Parent department is not self")  # 上级部门不能是自己
    employee_list_is_empty = _l("Employee list is empty")  # 员工列表为空

    column_name_not_support = _l("Column name not support")  # 不支持的列名
    password_is_required = _l("Password is required")  # 密码是必须的
    employee_acl_rid_is_zero = _l("Employee acl rid is zero")  # 员工ACL角色ID不能为0

    generate_excel_failed = _l("Generate excel failed: {}")  # 生成excel失败: {}
    rename_columns_failed = _l("Rename columns failed: {}")  # 重命名字段失败: {}
    cannot_block_this_employee_is_other_direct_supervisor = _l(
        "Cannot block this employee is other direct supervisor")  # 该员工是其他员工的直属上级, 不能禁用
    cannot_block_this_employee_is_department_manager = _l(
        "Cannot block this employee is department manager")  # 该员工是部门负责人, 不能禁用
    employee_id_not_found = _l("Employee id [{}] not found")  # 员工ID [{}] 不存在
    value_is_required = _l("Value is required")  # 值是必须的
    email_already_exists = _l("Email already exists")  # 邮箱已存在
    query_column_none_keep_value_empty = _l("Query {} none keep value empty")  # 查询 {} 空值时请保持value为空"
    not_support_operator = _l("Not support operator: {}")  # 不支持的操作符: {}
    not_support_relation = _l("Not support relation: {}")  # 不支持的关系: {}
    conditions_field_missing = _l("Conditions field missing")  # conditions内元素字段缺失，请检查！
    datetime_format_error = _l("Datetime format error: {}")  # {} 格式错误，应该为：%Y-%m-%d %H:%M:%S
    department_level_relation_error = _l("Department level relation error")  # 部门层级关系不正确
    delete_reserved_department_name = _l("Delete reserved department name")  # 保留部门，无法删除！
    department_id_is_required = _l("Department id is required")  # 部门ID是必须的
    department_list_is_required = _l("Department list is required")  # 部门列表是必须的
    cannot_to_be_parent_department = _l("{} Cannot to be parent department")  # 不能设置为上级部门
    department_id_not_found = _l("Department id [{}] not found")  # 部门ID [{}] 不存在
    parent_department_id_must_more_than_zero = _l("Parent department id must more than zero")  # 上级部门ID必须大于0
    department_name_already_exists = _l("Department name [{}] already exists")  # 部门名称 [{}] 已存在
    new_department_is_none = _l("New department is none")  # 新部门是空的

    acl_edit_user_failed = _l("ACL edit user failed: {}")  # ACL 修改用户失败: {}
    acl_uid_not_found = _l("ACL uid not found: {}")  # ACL 用户UID [{}] 不存在
    acl_add_user_failed = _l("ACL add user failed: {}")  # ACL 添加用户失败: {}
    acl_add_role_failed = _l("ACL add role failed: {}")  # ACL 添加角色失败: {}
    acl_update_role_failed = _l("ACL update role failed: {}")  # ACL 更新角色失败: {}
    acl_get_all_users_failed = _l("ACL get all users failed: {}")  # ACL 获取所有用户失败: {}
    acl_remove_user_from_role_failed = _l("ACL remove user from role failed: {}")  # ACL 从角色中移除用户失败: {}
    acl_add_user_to_role_failed = _l("ACL add user to role failed: {}")  # ACL 添加用户到角色失败: {}
    acl_import_user_failed = _l("ACL import user failed: {}")  # ACL 导入用户失败: {}

    nickname_is_required = _l("Nickname is required")  # 昵称不能为空
    username_is_required = _l("Username is required")  # 用户名不能为空
    email_is_required = _l("Email is required")  # 邮箱不能为空
    email_format_error = _l("Email format error")  # 邮箱格式错误
    email_send_timeout = _l("Email send timeout")  # 邮件发送超时

    common_data_not_found = _l("Common data not found {} ")  # ID {} 找不到记录
    common_data_already_existed = _l("Common data {} already existed")  # {} 已存在
    notice_platform_existed = _l("Notice platform {} existed")  # {} 已存在
    notice_not_existed = _l("Notice {} not existed")  # {} 配置项不存在
    notice_please_config_messenger_first = _l("Notice please config messenger first")  # 请先配置messenger URL
    notice_bind_err_with_empty_mobile = _l("Notice bind err with empty mobile")  # 绑定错误，手机号为空
    notice_bind_failed = _l("Notice bind failed: {}")  # 绑定失败: {}
    notice_bind_success = _l("Notice bind success")  # 绑定成功
    notice_remove_bind_success = _l("Notice remove bind success")  # 解绑成功

    not_support_test = _l("Not support test type: {}")  # 不支持的测试类型: {}
    not_support_auth_type = _l("Not support auth type: {}")  # 不支持的认证类型: {}
    ldap_server_connect_timeout = _l("LDAP server connect timeout")  # LDAP服务器连接超时
    ldap_server_connect_not_available = _l("LDAP server connect not available")  # LDAP服务器连接不可用
    ldap_test_unknown_error = _l("LDAP test unknown error: {}")  # LDAP测试未知错误: {}
    common_data_not_support_auth_type = _l("Common data not support auth type: {}")  # 通用数据不支持auth类型: {}
    ldap_test_username_required = _l("LDAP test username required")  # LDAP测试用户名必填

    company_wide = _l("Company wide")  # 全公司
