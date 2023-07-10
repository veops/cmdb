from api.lib.common_setting.utils import BaseEnum

COMMON_SETTING_QUEUE = "common_setting_async"


class OperatorType(BaseEnum):
    EQUAL = 1  # 等于
    NOT_EQUAL = 2  # 不等于
    IN = 3  # 包含
    NOT_IN = 4  # 不包含
    GREATER_THAN = 5  # 大于
    LESS_THAN = 6  # 小于
    IS_EMPTY = 7  # 为空
    IS_NOT_EMPTY = 8  # 不为空
