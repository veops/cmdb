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


class AuthenticateType(BaseEnum):
    CAS = 'CAS'
    OAUTH2 = 'OAUTH2'
    OIDC = 'OIDC'
    LDAP = 'LDAP'


AuthCommonConfig = 'AuthCommonConfig'
AuthCommonConfigAutoRedirect = 'auto_redirect'


class TestType(BaseEnum):
    Connect = 'connect'
    Login = 'login'


MIMEExtMap = {
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/msword': '.doc',
    'application/vnd.ms-word.document.macroEnabled.12': '.docm',
    'application/vnd.ms-excel': '.xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    'application/vnd.ms-excel.sheet.macroEnabled.12': '.xlsm',
    'application/vnd.ms-powerpoint': '.ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'application/vnd.ms-powerpoint.presentation.macroEnabled.12': '.pptm',
    'application/zip': '.zip',
    'application/x-7z-compressed': '.7z',
    'application/json': '.json',
    'application/pdf': '.pdf',
    'image/png': '.png',
    'image/bmp': '.bmp',
    'image/prs.btif': '.btif',
    'image/gif': '.gif',
    'image/jpeg': '.jpg',
    'image/tiff': '.tif',
    'image/vnd.microsoft.icon': '.ico',
    'image/webp': '.webp',
    'image/svg+xml': '.svg',
    'image/vnd.adobe.photoshop': '.psd',
    'text/plain': '.txt',
    'text/csv': '.csv',
}
