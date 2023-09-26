from api.models.common_setting import NoticeConfig
from wtforms import Form
from wtforms import StringField
from wtforms import validators
from flask import abort
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class NoticeConfigCRUD(object):

    @staticmethod
    def add_notice_config(**kwargs):
        NoticeConfigCRUD.check_platform(kwargs.get('platform'))
        try:
            return NoticeConfig.create(
                **kwargs
            )

        except Exception as e:
            return abort(400, str(e))

    @staticmethod
    def check_platform(platform):
        NoticeConfig.get_by(first=True, to_dict=False, platform=platform) and abort(400, f"{platform} 已存在！")

    @staticmethod
    def edit_notice_config(_id, **kwargs):
        existed = NoticeConfigCRUD.get_notice_config_by_id(_id)
        try:
            return existed.update(**kwargs)
        except Exception as e:
            return abort(400, str(e))

    @staticmethod
    def get_notice_config_by_id(_id):
        return NoticeConfig.get_by(first=True, to_dict=False, id=_id) or abort(400, f"{_id} 配置项不存在!")

    @staticmethod
    def get_all():
        return NoticeConfig.get_by(to_dict=True)

    @staticmethod
    def test_send_email(receive_address, **kwargs):
        # 设置发送方和接收方的电子邮件地址
        sender_email = 'test@test.com'
        sender_name = 'Test Sender'
        recipient_email = receive_address
        recipient_name = receive_address

        subject = 'Test Email'
        body = 'This is a test email'

        message = MIMEText(body, 'plain', 'utf-8')
        message['From'] = formataddr((sender_name, sender_email))
        message['To'] = formataddr((recipient_name, recipient_email))
        message['Subject'] = subject

        smtp_server = kwargs.get('server')
        smtp_port = kwargs.get('port')
        smtp_username = kwargs.get('username')
        smtp_password = kwargs.get('password')

        if kwargs.get('mail_type') == 'SMTP':
            smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        else:
            smtp_connection = smtplib.SMTP_SSL(smtp_server, smtp_port)

        if kwargs.get('is_login'):
            smtp_connection.login(smtp_username, smtp_password)

        smtp_connection.sendmail(sender_email, recipient_email, message.as_string())
        smtp_connection.quit()

        return 1


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
