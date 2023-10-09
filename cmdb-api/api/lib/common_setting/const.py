from api.lib.common_setting.utils import BaseEnum

COMMON_SETTING_QUEUE = "common_setting_async"


class OperatorType(BaseEnum):
    EQUAL = 1
    NOT_EQUAL = 2
    IN = 3
    NOT_IN = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    IS_EMPTY = 7
    IS_NOT_EMPTY = 8


BotNameMap = {
    'wechatApp': 'wechatBot',
    'feishuApp': 'feishuBot',
    'dingdingApp': 'dingdingBot',
}
