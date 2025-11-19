# -*- coding:utf-8 -*-

from flask_babel import lazy_gettext as _l


class CommonErrFormat(object):
    unauthorized = _l("unauthorized")  # Not authenticated
    unknown_error = _l("unknown error")  # Unknown error

    invalid_request = _l("Illegal request")  # Illegal request
    invalid_operation = _l("Invalid operation")  # Invalid operation

    not_found = _l("does not exist")  # Does not exist

    circular_dependency_error = _l("There is a circular dependency!")  # Circular dependency exists!

    unknown_search_error = _l("Unknown search error")  # Unknown search error

    # The json format seems to be incorrect, please confirm carefully!
    invalid_json = _l("The json format seems to be incorrect, please confirm carefully!")

    # The format of parameter {} is incorrect, the format must be: yyyy-mm-dd HH:MM:SS
    datetime_argument_invalid = _l("The format of parameter {} is incorrect, the format must be: yyyy-mm-dd HH:MM:SS")

    argument_value_required = _l("The value of parameter {} cannot be empty!")  # The value of parameter {} cannot be empty!
    argument_required = _l("The request is missing parameters {}")  # Request is missing parameters {}
    argument_invalid = _l("Invalid value for parameter {}")  # Invalid value for parameter {}
    argument_str_length_limit = _l("The length of parameter {} must be <= {}")  # The length of parameter {} must be <= {}

    role_required = _l("Role {} can only operate!")  # Only role {} can operate!
    user_not_found = _l("User {} does not exist")  # User {} does not exist
    no_permission = _l("For resource: {}, you do not have {} permission!")  # You do not have {} permission for resource: {}
    no_permission2 = _l("You do not have permission to operate!")  # You do not have permission to operate!
    no_permission_only_owner = _l("Only the creator or administrator has permission!")  # Only the creator or administrator has permission!
