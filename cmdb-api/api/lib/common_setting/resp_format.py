# -*- coding:utf-8 -*-
from flask_babel import lazy_gettext as _l

from api.lib.resp_format import CommonErrFormat


class ErrFormat(CommonErrFormat):
    company_info_is_already_existed = _l("Company info already existed")  # Company info already exists! Cannot create

    no_file_part = _l("No file part")  # No file part
    file_is_required = _l("File is required")  # File is required
    file_not_found = _l("File not found")  # File not found
    file_type_not_allowed = _l("File type not allowed")  # File type not allowed
    upload_failed = _l("Upload failed: {}")  # Upload failed: {}

    direct_supervisor_is_not_self = _l("Direct supervisor is not self")  # Direct supervisor cannot be self
    parent_department_is_not_self = _l("Parent department is not self")  # Parent department cannot be self
    employee_list_is_empty = _l("Employee list is empty")  # Employee list is empty

    column_name_not_support = _l("Column name not support")  # Unsupported column name
    password_is_required = _l("Password is required")  # Password is required
    employee_acl_rid_is_zero = _l("Employee acl rid is zero")  # Employee ACL role ID cannot be 0

    generate_excel_failed = _l("Generate excel failed: {}")  # Generate excel failed: {}
    rename_columns_failed = _l("Rename columns failed: {}")  # Rename columns failed: {}
    cannot_block_this_employee_is_other_direct_supervisor = _l(
        "Cannot block this employee is other direct supervisor")  # This employee is the direct supervisor of other employees and cannot be disabled
    cannot_block_this_employee_is_department_manager = _l(
        "Cannot block this employee is department manager")  # This employee is a department manager and cannot be disabled
    employee_id_not_found = _l("Employee id [{}] not found")  # Employee ID [{}] not found
    value_is_required = _l("Value is required")  # Value is required
    email_already_exists = _l("Email already exists")  # Email already exists
    query_column_none_keep_value_empty = _l("Query {} none keep value empty")  # When querying {} null value, please keep value empty
    not_support_operator = _l("Not support operator: {}")  # Unsupported operator: {}
    not_support_relation = _l("Not support relation: {}")  # Unsupported relation: {}
    conditions_field_missing = _l("Conditions field missing")  # Conditions field missing, please check!
    datetime_format_error = _l("Datetime format error: {}")  # {} format error, should be: %Y-%m-%d %H:%M:%S
    department_level_relation_error = _l("Department level relation error")  # Department level relation is incorrect
    delete_reserved_department_name = _l("Delete reserved department name")  # Reserved department, cannot be deleted!
    department_id_is_required = _l("Department id is required")  # Department ID is required
    department_list_is_required = _l("Department list is required")  # Department list is required
    cannot_to_be_parent_department = _l("{} Cannot to be parent department")  # Cannot be set as parent department
    department_id_not_found = _l("Department id [{}] not found")  # Department ID [{}] not found
    parent_department_id_must_more_than_zero = _l("Parent department id must more than zero")  # Parent department ID must be greater than 0
    department_name_already_exists = _l("Department name [{}] already exists")  # Department name [{}] already exists
    new_department_is_none = _l("New department is none")  # New department is empty

    acl_edit_user_failed = _l("ACL edit user failed: {}")  # ACL edit user failed: {}
    acl_uid_not_found = _l("ACL uid not found: {}")  # ACL user UID [{}] not found
    acl_add_user_failed = _l("ACL add user failed: {}")  # ACL add user failed: {}
    acl_add_role_failed = _l("ACL add role failed: {}")  # ACL add role failed: {}
    acl_update_role_failed = _l("ACL update role failed: {}")  # ACL update role failed: {}
    acl_get_all_users_failed = _l("ACL get all users failed: {}")  # ACL get all users failed: {}
    acl_remove_user_from_role_failed = _l("ACL remove user from role failed: {}")  # ACL remove user from role failed: {}
    acl_add_user_to_role_failed = _l("ACL add user to role failed: {}")  # ACL add user to role failed: {}
    acl_import_user_failed = _l("ACL import user failed: {}")  # ACL import user failed: {}

    nickname_is_required = _l("Nickname is required")  # Nickname cannot be empty
    username_is_required = _l("Username is required")  # Username cannot be empty
    email_is_required = _l("Email is required")  # Email cannot be empty
    email_format_error = _l("Email format error")  # Email format error
    email_send_timeout = _l("Email send timeout")  # Email send timeout

    common_data_not_found = _l("Common data not found {} ")  # ID {} record not found
    common_data_already_existed = _l("Common data {} already existed")  # {} already exists
    notice_platform_existed = _l("Notice platform {} existed")  # {} already exists
    notice_not_existed = _l("Notice {} not existed")  # {} configuration item does not exist
    notice_please_config_messenger_first = _l("Notice please config messenger first")  # Please configure messenger URL first
    notice_bind_err_with_empty_mobile = _l("Notice bind err with empty mobile")  # Bind error, mobile number is empty
    notice_bind_failed = _l("Notice bind failed: {}")  # Bind failed: {}
    notice_bind_success = _l("Notice bind success")  # Bind successful
    notice_remove_bind_success = _l("Notice remove bind success")  # Unbind successful

    not_support_test = _l("Not support test type: {}")  # Unsupported test type: {}
    not_support_auth_type = _l("Not support auth type: {}")  # Unsupported auth type: {}
    ldap_server_connect_timeout = _l("LDAP server connect timeout")  # LDAP server connection timeout
    ldap_server_connect_not_available = _l("LDAP server connect not available")  # LDAP server connection not available
    ldap_test_unknown_error = _l("LDAP test unknown error: {}")  # LDAP test unknown error: {}
    common_data_not_support_auth_type = _l("Common data not support auth type: {}")  # Common data does not support auth type: {}
    ldap_test_username_required = _l("LDAP test username required")  # LDAP test username required

    company_wide = _l("Company wide")  # Company wide

    resource_no_permission = _l("No permission to access resource {}, perm {} ")  # No permission to access {} resource's {} permission
