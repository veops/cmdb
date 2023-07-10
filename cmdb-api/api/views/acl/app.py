# -*- coding:utf-8 -*-

from flask import abort
from flask import request

from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.app import AppCRUD
from api.lib.perm.acl.resp_format import ErrFormat
from api.lib.perm.auth import auth_abandoned
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.resource import APIView


class AppView(APIView):
    url_prefix = ('/apps', '/apps/<int:_id>')

    def get(self, _id=None):
        if _id is not None:
            if not is_app_admin('acl'):
                return abort(403, ErrFormat.no_permission)

            app = AppCRUD.get(_id)
            app = app and app.to_dict() or {}

            return self.jsonify(**app)

        page = get_page(request.values.get('page', 1))
        page_size = get_page_size(request.values.get('page_size'))
        q = request.values.get('q')

        numfound, res = AppCRUD.search(q, page, page_size)

        res = [i.to_dict() for i in res]
        for i in res:
            i.pop('app_id', None)
            i.pop('secret_key', None)

        return self.jsonify(page=page,
                            page_size=page_size,
                            numfound=numfound,
                            total=len(res),
                            apps=res)

    @args_required('name')
    @args_validate(AppCRUD.cls)
    def post(self):
        name = request.values.get('name')
        description = request.values.get('description')

        app = AppCRUD.add(name, description)

        return self.jsonify(app.to_dict())

    @args_validate(AppCRUD.cls)
    def put(self, _id):
        app = AppCRUD.update(_id, **request.values)

        return self.jsonify(app.to_dict())

    def delete(self, _id):
        AppCRUD.delete(_id)

        return self.jsonify(id=_id)


class AppAccessTokenView(APIView):
    url_prefix = '/apps/token'

    @args_required('app_id')
    @args_required('secret_key')
    @auth_abandoned
    def post(self):
        token = AppCRUD.gen_token(request.values.get('app_id'), request.values.get('secret_key'))

        return self.jsonify(token=token)
