from flask import abort, request

from api.lib.perm.acl.acl import role_required
from api.resource import APIView
from api.lib.common_setting.common_data import AuthenticateDataCRUD
from api.lib.common_setting.resp_format import ErrFormat

prefix = '/auth_config'


class AuthConfigView(APIView):
    url_prefix = (f'{prefix}/<string:auth_type>',)

    @role_required("acl_admin")
    def get(self, auth_type):
        cli = AuthenticateDataCRUD(auth_type)

        if auth_type not in cli.get_support_type_list():
            abort(400, ErrFormat.not_support_auth_type.format(auth_type))

        if auth_type in cli.common_type_list:
            data = cli.get_record(True)
        else:
            data = cli.get_record_with_decrypt()
        return self.jsonify(data)

    @role_required("acl_admin")
    def post(self, auth_type):
        cli = AuthenticateDataCRUD(auth_type)

        if auth_type not in cli.get_support_type_list():
            abort(400, ErrFormat.not_support_auth_type.format(auth_type))

        params = request.json
        if auth_type in cli.common_type_list:
            params['encrypt'] = False
            cli.create(**params)
        else:
            cli.create(params.get('data', {}))

        return self.jsonify(params)


class AuthConfigViewWithId(APIView):
    url_prefix = (f'{prefix}/<string:auth_type>/<int:_id>',)

    @role_required("acl_admin")
    def put(self, auth_type, _id):
        cli = AuthenticateDataCRUD(auth_type)

        if auth_type not in cli.get_support_type_list():
            abort(400, ErrFormat.not_support_auth_type.format(auth_type))

        params = request.json
        data = params.get('data', {})
        if auth_type in cli.common_type_list:
            data['encrypt'] = False
            res = cli.update(_id, data)
        else:
            res = cli.update(_id, data)

        return self.jsonify(res.to_dict())

    @role_required("acl_admin")
    def delete(self, auth_type, _id):
        cli = AuthenticateDataCRUD(auth_type)

        if auth_type not in cli.get_support_type_list():
            abort(400, ErrFormat.not_support_auth_type.format(auth_type))
        cli.delete(_id)
        return self.jsonify({})


class AuthEnableListView(APIView):
    url_prefix = (f'{prefix}/enable_list',)

    method_decorators = []

    def get(self):
        return self.jsonify(AuthenticateDataCRUD.get_enable_list())


class AuthConfigTestView(APIView):
    url_prefix = (f'{prefix}/<string:auth_type>/test',)

    def post(self, auth_type):
        test_type = request.values.get('test_type', TestType.Connect)
        params = request.json
        return self.jsonify(AuthenticateDataCRUD(auth_type).test(test_type, params.get('data')))
