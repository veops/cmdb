# -*- coding:utf-8 -*-

from flask_babel import lazy_gettext as _l

from api.lib.resp_format import CommonErrFormat


class ErrFormat(CommonErrFormat):
    ci_type_config = _l("CI Model")  # 模型配置

    invalid_relation_type = _l("Invalid relation type: {}")  # 无效的关系类型: {}
    ci_type_not_found = _l("CIType is not found")  # 模型不存在!

    # 参数 attributes 类型必须是列表
    argument_attributes_must_be_list = _l("The type of parameter attributes must be a list")
    argument_file_not_found = _l("The file doesn't seem to be uploaded")  # 文件似乎并未上传

    attribute_not_found = _l("Attribute {} does not exist!")  # 属性 {} 不存在!
    attribute_is_unique_id = _l(
        "This attribute is the unique identifier of the model and cannot be deleted!")  # 该属性是模型的唯一标识，不能被删除!
    attribute_is_ref_by_type = _l(
        "This attribute is referenced by model {} and cannot be deleted!")  # 该属性被模型 {} 引用, 不能删除!
    attribute_value_type_cannot_change = _l(
        "The value type of the attribute is not allowed to be modified!")  # 属性的值类型不允许修改!
    attribute_list_value_cannot_change = _l("Multiple values are not allowed to be modified!")  # 多值不被允许修改!
    # 修改索引 非管理员不被允许!
    attribute_index_cannot_change = _l("Modifying the index is not allowed for non-administrators!")
    attribute_index_change_failed = _l("Index switching failed!")  # 索引切换失败!
    invalid_choice_values = _l("The predefined value is of the wrong type!")  # 预定义值的类型不对！
    attribute_name_duplicate = _l("Duplicate attribute name {}")  # 重复的属性名 {}
    add_attribute_failed = _l("Failed to create attribute {}!")  # 创建属性 {} 失败!
    update_attribute_failed = _l("Modify attribute {} failed!")  # 修改属性 {} 失败!
    cannot_edit_attribute = _l("You do not have permission to modify this attribute!")  # 您没有权限修改该属性!
    cannot_delete_attribute = _l(
        "Only creators and administrators are allowed to delete attributes!")  # 目前只允许 属性创建人、管理员 删除属性!
    # 属性字段名不能是内置字段: id, _id, ci_id, type, _type, ci_type
    attribute_name_cannot_be_builtin = _l(
        "Attribute field names cannot be built-in fields: id, _id, ci_id, type, _type, ci_type")
    attribute_choice_other_invalid = _l(
        "Predefined value: Other model request parameters are illegal!")  # 预定义值: 其他模型请求参数不合法!

    ci_not_found = _l("CI {} does not exist")  # CI {} 不存在
    unique_constraint = _l("Multiple attribute joint unique verification failed: {}")  # 多属性联合唯一校验不通过: {}
    unique_value_not_found = _l("The model's primary key {} does not exist!")  # 模型的主键 {} 不存在!
    unique_key_required = _l("Primary key {} is missing")  # 主键字段 {} 缺失
    ci_is_already_existed = _l("CI already exists!")  # CI 已经存在!
    relation_constraint = _l("Relationship constraint: {}, verification failed")  # 关系约束: {}, 校验失败
    # 多对多关系 限制: 模型 {} <-> {} 已经存在多对多关系!
    m2m_relation_constraint = _l(
        "Many-to-many relationship constraint: Model {} <-> {} already has a many-to-many relationship!")

    relation_not_found = _l("CI relationship: {} does not exist")  # CI关系: {} 不存在

    # 搜索表达式里小括号前不支持: 或、非
    ci_search_Parentheses_invalid = _l("In search expressions, not supported before parentheses: or, not")

    ci_type_not_found2 = _l("Model {} does not exist")  # 模型 {} 不存在
    ci_type_is_already_existed = _l("Model {} already exists")  # 模型 {} 已经存在
    unique_key_not_define = _l("The primary key is undefined or has been deleted")  # 主键未定义或者已被删除
    only_owner_can_delete = _l("Only the creator can delete it!")  # 只有创建人才能删除它!
    ci_exists_and_cannot_delete_type = _l(
        "The model cannot be deleted because the CI already exists")  # 因为CI已经存在，不能删除模型
    ci_exists_and_cannot_delete_inheritance = _l(
        "The inheritance cannot be deleted because the CI already exists")  # 因为CI已经存在，不能删除继承关系

    # 因为关系视图 {} 引用了该模型，不能删除模型
    ci_relation_view_exists_and_cannot_delete_type = _l(
        "The model cannot be deleted because the model is referenced by the relational view {}")
    ci_type_group_not_found = _l("Model group {} does not exist")  # 模型分组 {} 不存在
    ci_type_group_exists = _l("Model group {} already exists")  # 模型分组 {} 已经存在
    ci_type_relation_not_found = _l("Model relationship {} does not exist")  # 模型关系 {} 不存在
    ci_type_attribute_group_duplicate = _l("Attribute group {} already exists")  # 属性分组 {} 已存在
    ci_type_attribute_group_not_found = _l("Attribute group {} does not exist")  # 属性分组 {} 不存在
    # 属性组<{0}> - 属性<{1}> 不存在
    ci_type_group_attribute_not_found = _l("Attribute group <{0}> - attribute <{1}> does not exist")
    unique_constraint_duplicate = _l("The unique constraint already exists!")  # 唯一约束已经存在!
    # 唯一约束的属性不能是 JSON 和 多值
    unique_constraint_invalid = _l("Uniquely constrained attributes cannot be JSON and multi-valued")
    ci_type_trigger_duplicate = _l("Duplicated trigger")  # 重复的触发器
    ci_type_trigger_not_found = _l("Trigger {} does not exist")  # 触发器 {} 不存在

    record_not_found = _l("Operation record {} does not exist")  # 操作记录 {} 不存在
    cannot_delete_unique = _l("Unique identifier cannot be deleted")  # 不能删除唯一标识
    cannot_delete_default_order_attr = _l("Cannot delete default sorted attributes")  # 不能删除默认排序的属性

    preference_relation_view_node_required = _l("No node selected")  # 没有选择节点
    preference_search_option_not_found = _l("This search option does not exist!")  # 该搜索选项不存在!
    preference_search_option_exists = _l("This search option has a duplicate name!")  # 该搜索选项命名重复!

    relation_type_exists = _l("Relationship type {} already exists")  # 关系类型 {} 已经存在
    relation_type_not_found = _l("Relationship type {} does not exist")  # 关系类型 {} 不存在

    attribute_value_invalid = _l("Invalid attribute value: {}")  # 无效的属性值: {}
    attribute_value_invalid2 = _l("{} Invalid value: {}")  # {} 无效的值: {}
    not_in_choice_values = _l("{} is not in the predefined values")  # {} 不在预定义值里
    # 属性 {} 的值必须是唯一的, 当前值 {} 已存在
    attribute_value_unique_required = _l("The value of attribute {} must be unique, {} already exists")
    attribute_value_required = _l("Attribute {} value must exist")  # 属性 {} 值必须存在
    attribute_value_out_of_range = _l("Out of range value, the maximum value is 2147483647")
    # 新增或者修改属性值未知错误: {}
    attribute_value_unknown_error = _l("Unknown error when adding or modifying attribute value: {}")

    custom_name_duplicate = _l("Duplicate custom name")  # 订制名重复

    limit_ci_type = _l("Number of models exceeds limit: {}")  # 模型数超过限制: {}
    limit_ci = _l("The number of CIs exceeds the limit: {}")  # CI数超过限制: {}

    adr_duplicate = _l("Auto-discovery rule: {} already exists!")  # 自动发现规则: {} 已经存在!
    adr_not_found = _l("Auto-discovery rule: {} does not exist!")  # 自动发现规则: {} 不存在!
    # 该自动发现规则被模型引用, 不能删除!
    adr_referenced = _l("This auto-discovery rule is referenced by the model and cannot be deleted!")
    # 自动发现规则的应用不能重复定义!
    ad_duplicate = _l("The application of auto-discovery rules cannot be defined repeatedly!")
    ad_not_found = _l("The auto-discovery you want to modify: {} does not exist!")  # 您要修改的自动发现: {} 不存在!
    ad_not_unique_key = _l("Attribute does not include unique identifier: {}")  # 属性字段没有包括唯一标识: {}
    adc_not_found = _l("The auto-discovery instance does not exist!")  # 自动发现的实例不存在!
    adt_not_found = _l("The model is not associated with this auto-discovery!")  # 模型并未关联该自动发现!
    adt_secret_no_permission = _l("Only the creator can modify the Secret!")  # 只有创建人才能修改Secret!
    # 该规则已经有自动发现的实例, 不能被删除!
    cannot_delete_adt = _l("This rule already has auto-discovery instances and cannot be deleted!")
    # 该默认的自动发现规则 已经被模型 {} 引用!
    adr_default_ref_once = _l("The default auto-discovery rule is already referenced by model {}!")
    # unique_key方法必须返回非空字符串!
    adr_unique_key_required = _l("The unique_key method must return a non-empty string!")
    adr_plugin_attributes_list_required = _l("The attributes method must return a list")  # attributes方法必须返回的是list
    # attributes方法返回的list不能为空!
    adr_plugin_attributes_list_no_empty = _l("The list returned by the attributes method cannot be empty!")
    # 只有管理员才可以定义执行机器为: 所有节点!
    adt_target_all_no_permission = _l("Only administrators can define execution targets as: all nodes!")
    adt_target_expr_no_permission = _l("Execute targets permission check failed: {}")  # 执行机器权限检查不通过: {}

    ci_filter_name_cannot_be_empty = _l("CI filter authorization must be named!")  # CI过滤授权 必须命名!
    ci_filter_perm_cannot_or_query = _l(
        "CI filter authorization is currently not supported or query")  # CI过滤授权 暂时不支持 或 查询
    # 您没有属性 {} 的操作权限!
    ci_filter_perm_attr_no_permission = _l("You do not have permission to operate attribute {}!")
    ci_filter_perm_ci_no_permission = _l("You do not have permission to operate this CI!")  # 您没有该CI的操作权限!

    password_save_failed = _l("Failed to save password: {}")  # 保存密码失败: {}
    password_load_failed = _l("Failed to get password: {}")  # 获取密码失败: {}
