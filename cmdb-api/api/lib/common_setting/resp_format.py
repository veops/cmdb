# -*- coding:utf-8 -*-

from api.lib.resp_format import CommonErrFormat


class ErrFormat(CommonErrFormat):
    company_info_is_already_existed = "公司信息已存在！无法创建"

    no_file_part = "没有文件部分"
    file_is_required = "文件是必须的"
    file_not_found = "文件不存在"
    file_type_not_allowed = "文件类型不允许"
    upload_failed = "上传失败: {}"

    direct_supervisor_is_not_self = "直属上级不能是自己"
    parent_department_is_not_self = "上级部门不能是自己"
    employee_list_is_empty = "员工列表为空"

    column_name_not_support = "不支持的列名"
    password_is_required = "密码不能为空"
    employee_acl_rid_is_zero = "员工ACL角色ID不能为0"

    generate_excel_failed = "生成excel失败: {}"
    rename_columns_failed = "字段转换为中文失败: {}"
    cannot_block_this_employee_is_other_direct_supervisor = "该员工是其他员工的直属上级, 不能禁用"
    cannot_block_this_employee_is_department_manager = "该员工是部门负责人, 不能禁用"
    employee_id_not_found = "员工ID [{}] 不存在"
    value_is_required = "值是必须的"
    email_already_exists = "邮箱 [{}] 已存在"
    query_column_none_keep_value_empty = "查询 {} 空值时请保持value为空"
    not_support_operator = "不支持的操作符: {}"
    not_support_relation = "不支持的关系: {}"
    conditions_field_missing = "conditions内元素字段缺失，请检查！"
    datetime_format_error = "{} 格式错误，应该为：%Y-%m-%d %H:%M:%S"
    department_level_relation_error = "部门层级关系不正确"
    delete_reserved_department_name = "保留部门，无法删除！"
    department_id_is_required = "部门ID是必须的"
    department_list_is_required = "部门列表是必须的"
    cannot_to_be_parent_department = "{} 不能设置为上级部门"
    department_id_not_found = "部门ID [{}] 不存在"
    parent_department_id_must_more_than_zero = "上级部门ID必须大于0"
    department_name_already_exists = "部门名称 [{}] 已存在"
    new_department_is_none = "新部门是空的"

    acl_edit_user_failed = "ACL 修改用户失败: {}"
    acl_uid_not_found = "ACL 用户UID [{}] 不存在"
    acl_add_user_failed = "ACL 添加用户失败: {}"
    acl_add_role_failed = "ACL 添加角色失败: {}"
    acl_update_role_failed = "ACL 更新角色失败: {}"
    acl_get_all_users_failed = "ACL 获取所有用户失败: {}"
    acl_remove_user_from_role_failed = "ACL 从角色中移除用户失败: {}"
    acl_add_user_to_role_failed = "ACL 添加用户到角色失败: {}"
    acl_import_user_failed = "ACL 导入用户[{}]失败: {}"

    nickname_is_required = "用户名不能为空"
    username_is_required = "username不能为空"
    email_is_required = "邮箱不能为空"
    email_format_error = "邮箱格式错误"
    email_send_timeout = "邮件发送超时"

    common_data_not_found = "ID {} 找不到记录"
    notice_platform_existed = "{} 已存在"
    notice_not_existed = "{} 配置项不存在"
    notice_please_config_messenger_first = "请先配置 messenger"
    notice_bind_err_with_empty_mobile = "绑定失败，手机号为空"
    notice_bind_failed = "绑定失败: {}"
    notice_bind_success = "绑定成功"
    notice_remove_bind_success = "解绑成功"

    not_support_test = "不支持的测试类型: {}"
    not_support_auth_type = "不支持的认证类型: {}"
    ldap_server_connect_timeout = "LDAP服务器连接超时"
    ldap_test_unknown_error = "LDAP测试未知错误: {}"
    common_data_not_support_auth_type = "通用数据不支持auth类型: {}"

