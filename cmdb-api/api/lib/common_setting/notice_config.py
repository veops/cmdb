import requests

from api.lib.common_setting.const import BotNameMap
from api.lib.common_setting.resp_format import ErrFormat
from api.models.common_setting import CompanyInfo, NoticeConfig
from wtforms import Form
from wtforms import StringField
from wtforms import validators
from flask import abort, current_app


class NoticeConfigCRUD(object):

    @staticmethod
    def add_notice_config(**kwargs):
        platform = kwargs.get('platform')
        NoticeConfigCRUD.check_platform(platform)
        info = kwargs.get('info', {})
        if 'name' not in info:
            info['name'] = platform
        kwargs['info'] = info
        try:
            NoticeConfigCRUD.update_messenger_config(**info)
            res = NoticeConfig.create(
                **kwargs
            )
            return res

        except Exception as e:
            return abort(400, str(e))

    @staticmethod
    def check_platform(platform):
        NoticeConfig.get_by(first=True, to_dict=False, platform=platform) and \
        abort(400, ErrFormat.notice_platform_existed.format(platform))

    @staticmethod
    def edit_notice_config(_id, **kwargs):
        existed = NoticeConfigCRUD.get_notice_config_by_id(_id)
        try:
            info = kwargs.get('info', {})
            if 'name' not in info:
                info['name'] = existed.platform
            kwargs['info'] = info
            NoticeConfigCRUD.update_messenger_config(**info)

            res = existed.update(**kwargs)
            return res
        except Exception as e:
            return abort(400, str(e))

    @staticmethod
    def get_messenger_url():
        from api.lib.common_setting.company_info import CompanyInfoCache
        com_info = CompanyInfoCache.get()
        if not com_info:
            return
        messenger = com_info.get('messenger', '')
        if len(messenger) == 0:
            return
        if messenger[-1] == '/':
            messenger = messenger[:-1]
        return messenger

    @staticmethod
    def update_messenger_config(**kwargs):
        try:
            messenger = NoticeConfigCRUD.get_messenger_url()
            if not messenger or len(messenger) == 0:
                raise Exception(ErrFormat.notice_please_config_messenger_first)

            url = f"{messenger}/v1/senders"
            name = kwargs.get('name')
            bot_list = kwargs.pop('bot', None)
            for k, v in kwargs.items():
                if isinstance(v, bool):
                    kwargs[k] = 'true' if v else 'false'
                else:
                    kwargs[k] = str(v)

            payload = {name: [kwargs]}
            current_app.logger.info(f"update_messenger_config: {url}, {payload}")
            res = requests.put(url, json=payload, timeout=2)
            current_app.logger.info(f"update_messenger_config: {res.status_code}, {res.text}")

            if not bot_list or len(bot_list) == 0:
                return
            bot_name = BotNameMap.get(name)
            payload = {bot_name: bot_list}
            current_app.logger.info(f"update_messenger_config: {url}, {payload}")
            bot_res = requests.put(url, json=payload, timeout=2)
            current_app.logger.info(f"update_messenger_config: {bot_res.status_code}, {bot_res.text}")

        except Exception as e:
            return abort(400, str(e))

    @staticmethod
    def get_notice_config_by_id(_id):
        return NoticeConfig.get_by(first=True, to_dict=False, id=_id) or \
            abort(400,
                  ErrFormat.notice_not_existed.format(_id))

    @staticmethod
    def get_all():
        return NoticeConfig.get_by(to_dict=True)

    @staticmethod
    def test_send_email(receive_address, **kwargs):
        messenger = NoticeConfigCRUD.get_messenger_url()
        if not messenger or len(messenger) == 0:
            abort(400, ErrFormat.notice_please_config_messenger_first)
        url = f"{messenger}/v1/message"

        recipient_email = receive_address

        subject = 'Test Email'
        body = 'This is a test email'
        payload = {
            "sender": 'email',
            "msgtype": "text/plain",
            "title": subject,
            "content": body,
            "tos": [recipient_email],
        }
        current_app.logger.info(f"test_send_email: {url}, {payload}")
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            abort(400, response.text)

        return 1

    @staticmethod
    def get_app_bot():
        result = []
        for notice_app in NoticeConfig.get_by(to_dict=False):
            if notice_app.platform in ['email']:
                continue
            info = notice_app.info
            name = info.get('name', '')
            if name not in BotNameMap:
                continue
            result.append(dict(
                name=info.get('name', ''),
                label=info.get('label', ''),
                bot=info.get('bot', []),
            ))
        return result


class NoticeConfigForm(Form):
    platform = StringField(validators=[
        validators.DataRequired(message="平台 不能为空"),
        validators.Length(max=255),
    ])
    info = StringField(validators=[
        validators.DataRequired(message="信息 不能为空"),
        validators.Length(max=255),
    ])


class NoticeConfigUpdateForm(Form):
    info = StringField(validators=[
        validators.DataRequired(message="信息 不能为空"),
        validators.Length(max=255),
    ])