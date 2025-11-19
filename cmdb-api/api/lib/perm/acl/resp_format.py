# -*- coding:utf-8 -*-

from flask_babel import lazy_gettext as _l

from api.lib.resp_format import CommonErrFormat


class ErrFormat(CommonErrFormat):
    login_succeed = _l("login successful")  # Login successful
    ldap_connection_failed = _l("Failed to connect to LDAP service")  # Failed to connect to LDAP service
    invalid_password = _l("Password verification failed")  # Password verification failed
    auth_only_with_app_token_failed = _l("Application Token verification failed")  # Application Token verification failed
    # You are not the application administrator or the session has expired (try logging out and logging in again)
    session_invalid = _l(
        "You are not the application administrator or the session has expired (try logging out and logging in again)")

    resource_type_not_found = _l("Resource type {} does not exist!")  # Resource type {} does not exist!
    resource_type_exists = _l("Resource type {} already exists!")  # Resource type {} already exists!
    # Because there are resources under this type, they cannot be deleted!
    resource_type_cannot_delete = _l("Because there are resources under this type, they cannot be deleted!")

    user_not_found = _l("User {} does not exist!")  # User {} does not exist!
    user_exists = _l("User {} already exists!")  # User {} already exists!
    role_not_found = _l("Role {} does not exist!")  # Role {} does not exist!
    role_exists = _l("Role {} already exists!")  # Role {} already exists!
    global_role_not_found = _l("Global role {} does not exist!")  # Global role {} does not exist!
    global_role_exists = _l("Global role {} already exists!")  # Global role {} already exists!

    resource_no_permission = _l("You do not have {} permission on resource: {}")  # You do not have {} permission on resource: {}
    admin_required = _l("Requires administrator permissions")  # Requires administrator permissions
    role_required = _l("Requires role: {}")  # Requires role: {}
    # To delete a user role, please operate on the User Management page!
    user_role_delete_invalid = _l("To delete a user role, please operate on the User Management page!")

    app_is_ready_existed = _l("Application {} already exists")  # Application {} already exists
    app_not_found = _l("Application {} does not exist!")  # Application {} does not exist!
    app_secret_invalid = _l("The Secret is invalid")  # The application's Secret is invalid

    resource_not_found = _l("Resource {} does not exist!")  # Resource {} does not exist!
    resource_exists = _l("Resource {} already exists!")  # Resource {} already exists!

    resource_group_not_found = _l("Resource group {} does not exist!")  # Resource group {} does not exist!
    resource_group_exists = _l("Resource group {} already exists!")  # Resource group {} already exists!

    inheritance_dead_loop = _l("Inheritance detected infinite loop")  # Inheritance detected infinite loop
    role_relation_not_found = _l("Role relationship {} does not exist!")  # Role relationship {} does not exist!

    trigger_not_found = _l("Trigger {} does not exist!")  # Trigger {} does not exist!
    trigger_exists = _l("Trigger {} already exists!")  # Trigger {} already exists!
    trigger_disabled = _l("Trigger {} has been disabled!")  # Trigger {} has been disabled!
