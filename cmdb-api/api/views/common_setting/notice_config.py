from flask import request, abort, current_app
from werkzeug.datastructures import MultiDict

from api.lib.perm.auth import auth_with_app_token
from api.models.common_setting import NoticeConfig
from api.resource import APIView
from api.lib.common_setting.notice_config import NoticeConfigForm, NoticeConfigUpdateForm, NoticeConfigCRUD
from api.lib.decorator import args_required
from api.lib.common_setting.resp_format import ErrFormat

prefix = '/notice_config'


class NoticeConfigView(APIView):
    url_prefix = (f'{prefix}',)

    @args_required('platform')
    @auth_with_app_token
    def get(self):
        platform = request.args.get('platform')
        res = NoticeConfig.get_by(first=True, to_dict=True, platform=platform) or {}
        return self.jsonify(res)

    def post(self):
        form = NoticeConfigForm(MultiDict(request.json))
        if not form.validate():
            abort(400, ','.join(['{}: {}'.format(filed, ','.join(msg)) for filed, msg in form.errors.items()]))

        data = NoticeConfigCRUD.add_notice_config(**form.data)
        return self.jsonify(data.to_dict())


class NoticeConfigUpdateView(APIView):
    url_prefix = (f'{prefix}/<int:_id>',)

    def put(self, _id):
        form = NoticeConfigUpdateForm(MultiDict(request.json))
        if not form.validate():
            abort(400, ','.join(['{}: {}'.format(filed, ','.join(msg)) for filed, msg in form.errors.items()]))

        data = NoticeConfigCRUD.edit_notice_config(_id, **form.data)
        return self.jsonify(data.to_dict())


class CheckEmailServer(APIView):
    url_prefix = (f'{prefix}/send_test_email',)

    def post(self):
        receive_address = request.args.get('receive_address')
        info = request.values.get('info')

        try:

            result = NoticeConfigCRUD.test_send_email(receive_address, **info)
            return self.jsonify(result=result)
        except Exception as e:
            current_app.logger.error('test_send_email err:')
            current_app.logger.error(e)
            if 'Timed Out' in str(e):
                abort(400, ErrFormat.email_send_timeout)
            abort(400, f"{str(e)}")


class NoticeConfigGetView(APIView):
    method_decorators = []
    url_prefix = (f'{prefix}/all',)

    @auth_with_app_token
    def get(self):
        res = NoticeConfigCRUD.get_all()
        return self.jsonify(res)


class NoticeAppBotView(APIView):
    url_prefix = (f'{prefix}/app_bot',)

    def get(self):
        res = NoticeConfigCRUD.get_app_bot()
        return self.jsonify(res)
