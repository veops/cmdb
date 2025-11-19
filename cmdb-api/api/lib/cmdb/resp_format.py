# -*- coding:utf-8 -*-

from flask_babel import lazy_gettext as _l

from api.lib.resp_format import CommonErrFormat


class ErrFormat(CommonErrFormat):
    ci_type_config = _l("CI Model")  # Model configuration

    invalid_relation_type = _l("Invalid relation type: {}")  # Invalid relation type: {}
    ci_type_not_found = _l("CIType is not found")  # Model does not exist!

    # The type of parameter attributes must be a list
    argument_attributes_must_be_list = _l("The type of parameter attributes must be a list")
    argument_file_not_found = _l("The file doesn't seem to be uploaded")  # The file doesn't seem to be uploaded

    attribute_not_found = _l("Attribute {} does not exist!")  # Attribute {} does not exist!
    # This attribute is the unique identifier of the model and cannot be deleted!
    attribute_is_unique_id = _l(
        "This attribute is the unique identifier of the model and cannot be deleted!")
    attribute_is_ref_by_type = _l(
        "This attribute is referenced by model {} and cannot be deleted!")  # This attribute is referenced by model {}, cannot be deleted!
    attribute_value_type_cannot_change = _l(
        "The value type of the attribute is not allowed to be modified!")  # The value type of the attribute is not allowed to be modified!
    attribute_list_value_cannot_change = _l("Multiple values are not allowed to be modified!")  # Multiple values are not allowed to be modified!
    # Modifying the index is not allowed for non-administrators!
    attribute_index_cannot_change = _l("Modifying the index is not allowed for non-administrators!")
    attribute_index_change_failed = _l("Index switching failed!")  # Index switching failed!
    invalid_choice_values = _l("The predefined value is of the wrong type!")  # The predefined value is of the wrong type!
    attribute_name_duplicate = _l("Duplicate attribute name {}")  # Duplicate attribute name {}
    add_attribute_failed = _l("Failed to create attribute {}!")  # Failed to create attribute {}!
    update_attribute_failed = _l("Modify attribute {} failed!")  # Modify attribute {} failed!
    cannot_edit_attribute = _l("You do not have permission to modify this attribute!")  # You do not have permission to modify this attribute!
    cannot_delete_attribute = _l(
        "Only creators and administrators are allowed to delete attributes!")  # Currently only attribute creators and administrators are allowed to delete attributes!
    # Attribute field names cannot be built-in fields: id, _id, ci_id, type, _type, ci_type
    attribute_name_cannot_be_builtin = _l(
        "Attribute field names cannot be built-in fields: id, _id, ci_id, type, _type, ci_type, ticket_id")
    attribute_choice_other_invalid = _l(
        "Predefined value: Other model request parameters are illegal!")  # Predefined value: Other model request parameters are illegal!

    ci_not_found = _l("CI {} does not exist")  # CI {} does not exist
    unique_constraint = _l("Multiple attribute joint unique verification failed: {}")  # Multiple attribute joint unique verification failed: {}
    unique_value_not_found = _l("The model's primary key {} does not exist!")  # The model's primary key {} does not exist!
    unique_key_required = _l("Primary key {} is missing")  # Primary key field {} is missing
    ci_is_already_existed = _l("CI already exists!")  # CI already exists!
    ci_reference_not_found = _l("{}: CI reference {} does not exist!")  # {}: CI reference {} does not exist!
    ci_reference_invalid = _l("{}: CI reference {} is illegal!")  # {}: CI reference {} is illegal!
    relation_constraint = _l("Relationship constraint: {}, verification failed")  # Relationship constraint: {}, verification failed
    # Many-to-many relationship constraint: Model {} <-> {} already has a many-to-many relationship!
    m2m_relation_constraint = _l(
        "Many-to-many relationship constraint: Model {} <-> {} already has a many-to-many relationship!")

    relation_not_found = _l("CI relationship: {} does not exist")  # CI relationship: {} does not exist

    # In search expressions, not supported before parentheses: or, not
    ci_search_Parentheses_invalid = _l("In search expressions, not supported before parentheses: or, not")

    ci_type_not_found2 = _l("Model {} does not exist")  # Model {} does not exist
    ci_type_is_already_existed = _l("Model {} already exists")  # Model {} already exists
    unique_key_not_define = _l("The primary key is undefined or has been deleted")  # The primary key is undefined or has been deleted
    only_owner_can_delete = _l("Only the creator can delete it!")  # Only the creator can delete it!
    ci_exists_and_cannot_delete_type = _l(
        "The model cannot be deleted because the CI already exists")  # The model cannot be deleted because the CI already exists
    ci_exists_and_cannot_delete_inheritance = _l(
        "The inheritance cannot be deleted because the CI already exists")  # The inheritance cannot be deleted because the CI already exists
    ci_type_inheritance_cannot_delete = _l("The model is inherited and cannot be deleted")  # This model is inherited and cannot be deleted
    ci_type_referenced_cannot_delete = _l(
        "The model is referenced by attribute {} and cannot be deleted")  # This model is referenced by attribute {} and cannot be deleted

    # The model cannot be deleted because the model is referenced by the relational view {}
    ci_relation_view_exists_and_cannot_delete_type = _l(
        "The model cannot be deleted because the model is referenced by the relational view {}")
    ci_type_group_not_found = _l("Model group {} does not exist")  # Model group {} does not exist
    ci_type_group_exists = _l("Model group {} already exists")  # Model group {} already exists
    ci_type_relation_not_found = _l("Model relationship {} does not exist")  # Model relationship {} does not exist
    ci_type_attribute_group_duplicate = _l("Attribute group {} already exists")  # Attribute group {} already exists
    ci_type_attribute_group_not_found = _l("Attribute group {} does not exist")  # Attribute group {} does not exist
    # Attribute group <{0}> - attribute <{1}> does not exist
    ci_type_group_attribute_not_found = _l("Attribute group <{0}> - attribute <{1}> does not exist")
    unique_constraint_duplicate = _l("The unique constraint already exists!")  # The unique constraint already exists!
    # Uniquely constrained attributes cannot be JSON and multi-valued
    unique_constraint_invalid = _l("Uniquely constrained attributes cannot be JSON and multi-valued")
    ci_type_trigger_duplicate = _l("Duplicated trigger")  # Duplicated trigger
    ci_type_trigger_not_found = _l("Trigger {} does not exist")  # Trigger {} does not exist
    ci_type_reconciliation_duplicate = _l("Duplicated reconciliation rule")  # Duplicated reconciliation rule
    ci_type_reconciliation_not_found = _l("Reconciliation rule {} does not exist")  # Reconciliation rule {} does not exist

    record_not_found = _l("Operation record {} does not exist")  # Operation record {} does not exist
    cannot_delete_unique = _l("Unique identifier cannot be deleted")  # Cannot delete unique identifier
    cannot_delete_default_order_attr = _l("Cannot delete default sorted attributes")  # Cannot delete default sorted attributes

    preference_relation_view_node_required = _l("No node selected")  # No node selected
    preference_search_option_not_found = _l("This search option does not exist!")  # This search option does not exist!
    preference_search_option_exists = _l("This search option has a duplicate name!")  # This search option has a duplicate name!

    relation_type_exists = _l("Relationship type {} already exists")  # Relationship type {} already exists
    relation_type_not_found = _l("Relationship type {} does not exist")  # Relationship type {} does not exist

    attribute_value_invalid = _l("Invalid attribute value: {}")  # Invalid attribute value: {}
    attribute_value_invalid2 = _l("{} Invalid value: {}")  # {} Invalid value: {}
    not_in_choice_values = _l("{} is not in the predefined values")  # {} is not in the predefined values
    # The value of attribute {} must be unique, current value {} already exists
    attribute_value_unique_required = _l("The value of attribute {} must be unique, {} already exists")
    attribute_value_required = _l("Attribute {} value must exist")  # Attribute {} value must exist
    attribute_value_out_of_range = _l("Out of range value, the maximum value is 2147483647")
    # Unknown error when adding or modifying attribute value: {}
    attribute_value_unknown_error = _l("Unknown error when adding or modifying attribute value: {}")

    custom_name_duplicate = _l("Duplicate custom name")  # Duplicate custom name

    limit_ci_type = _l("Number of models exceeds limit: {}")  # Number of models exceeds limit: {}
    limit_ci = _l("The number of CIs exceeds the limit: {}")  # The number of CIs exceeds the limit: {}

    adr_duplicate = _l("Auto-discovery rule: {} already exists!")  # Auto-discovery rule: {} already exists!
    adr_not_found = _l("Auto-discovery rule: {} does not exist!")  # Auto-discovery rule: {} does not exist!
    # This auto-discovery rule is referenced by the model and cannot be deleted!
    adr_referenced = _l("This auto-discovery rule is referenced by the model and cannot be deleted!")
    # The application of auto-discovery rules cannot be defined repeatedly!
    ad_duplicate = _l("The application of auto-discovery rules cannot be defined repeatedly!")
    ad_not_found = _l("The auto-discovery you want to modify: {} does not exist!")  # The auto-discovery you want to modify: {} does not exist!
    ad_not_unique_key = _l("Attribute does not include unique identifier: {}")  # Attribute field does not include unique identifier: {}
    adc_not_found = _l("The auto-discovery instance does not exist!")  # The auto-discovery instance does not exist!
    adt_not_found = _l("The model is not associated with this auto-discovery!")  # The model is not associated with this auto-discovery!
    adt_secret_no_permission = _l("Only the creator can modify the Secret!")  # Only the creator can modify the Secret!
    # This rule already has auto-discovery instances and cannot be deleted!
    cannot_delete_adt = _l("This rule already has auto-discovery instances and cannot be deleted!")
    # The default auto-discovery rule is already referenced by model {}!
    adr_default_ref_once = _l("The default auto-discovery rule is already referenced by model {}!")
    # The unique_key method must return a non-empty string!
    adr_unique_key_required = _l("The unique_key method must return a non-empty string!")
    # The attributes method must return a list
    adr_plugin_attributes_list_required = _l("The attributes method must return a list")
    # The list returned by the attributes method cannot be empty!
    adr_plugin_attributes_list_no_empty = _l("The list returned by the attributes method cannot be empty!")
    # Only administrators can define execution targets as: all nodes!
    adt_target_all_no_permission = _l("Only administrators can define execution targets as: all nodes!")
    adt_target_expr_no_permission = _l("Execute targets permission check failed: {}")  # Execute targets permission check failed: {}

    ci_filter_name_cannot_be_empty = _l("CI filter authorization must be named!")  # CI filter authorization must be named!
    ci_filter_perm_cannot_or_query = _l(
        "CI filter authorization is currently not supported or query")  # CI filter authorization currently does not support OR query
    # You do not have permission to operate attribute {}!
    ci_filter_perm_attr_no_permission = _l("You do not have permission to operate attribute {}!")
    ci_filter_perm_ci_no_permission = _l("You do not have permission to operate this CI!")  # You do not have permission to operate this CI!

    password_save_failed = _l("Failed to save password: {}")  # Failed to save password: {}
    password_load_failed = _l("Failed to get password: {}")  # Failed to get password: {}

    cron_time_format_invalid = _l("Scheduling time format error")  # Scheduling time format error
    reconciliation_title = _l("CMDB data reconciliation results")  # CMDB data reconciliation results
    reconciliation_body = _l("Number of {} illegal: {}")  # Number of {} non-compliant: {}

    topology_exists = _l("Topology view {} already exists")  # Topology view {} already exists
    topology_group_exists = _l("Topology group {} already exists")  # Topology group {} already exists
    # The group cannot be deleted because the topology view already exists
    topo_view_exists_cannot_delete_group = _l("The group cannot be deleted because the topology view already exists")

    relation_path_search_src_target_required = _l("Both the source model and the target model must be selected")

    builtin_type_cannot_update_name = _l("The names of built-in models cannot be changed")
    # # IPAM
    ipam_subnet_model_not_found = _l("The subnet model {} does not exist")
    ipam_address_model_not_found = _l("The IP Address model {} does not exist")
    ipam_cidr_invalid_notation = _l("CIDR {} is an invalid notation")
    ipam_cidr_invalid_subnet = _l("Invalid CIDR: {}, available subnets: {}")
    ipam_subnet_prefix_length_invalid = _l("Invalid subnet prefix length: {}")
    ipam_parent_subnet_node_cidr_cannot_empty = _l("parent node cidr must be required")
    ipam_subnet_overlapped = _l("{} and {} overlap")
    ipam_subnet_cannot_delete = _l("Cannot delete because child nodes exist")
    ipam_subnet_not_found = _l("Subnet is not found")
    ipam_scope_cannot_delete = _l("Cannot delete because child nodes exist")

    # # DCIM
    dcim_builtin_model_not_found = _l("The dcim model {} does not exist")
    dcim_rack_u_slot_invalid = _l("Irregularities in Rack Units")
    dcim_rack_u_count_invalid = _l("The device's position is greater than the rack unit height")
