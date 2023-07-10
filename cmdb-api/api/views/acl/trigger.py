# -*- coding:utf-8 -*-

from flask import request

from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl import validate_app
from api.lib.perm.acl.trigger import TriggerCRUD
from api.lib.perm.auth import auth_only_for_acl
from api.lib.perm.auth import auth_with_app_token
from api.resource import APIView


class TriggerView(APIView):
    url_prefix = ("/triggers", "/triggers/<int:_id>")

    @validate_app
    @auth_with_app_token
    def get(self):
        return self.jsonify(TriggerCRUD.get(request.values.get('app_id')))

    @args_required('name')
    @args_required('resource_type_id')
    @args_required('roles')
    @args_required('permissions')
    @validate_app
    @auth_only_for_acl
    @args_validate(TriggerCRUD.cls, exclude_args=['app_id'])
    def post(self):
        request.values.pop('_key', None)
        request.values.pop('_secret', None)
        trigger = TriggerCRUD.add(request.values.pop('app_id', None), **request.values)

        return self.jsonify(trigger.to_dict())

    @args_required('resource_type_id')
    @args_required('roles')
    @args_required('permissions')
    @validate_app
    @auth_only_for_acl
    @args_validate(TriggerCRUD.cls, exclude_args=['app_id'])
    def put(self, _id):
        request.values.pop('_key', None)
        request.values.pop('_secret', None)

        trigger = TriggerCRUD.update(_id, **request.values)

        return self.jsonify(trigger.to_dict())

    @auth_only_for_acl
    def delete(self, _id):
        TriggerCRUD.delete(_id)

        return self.jsonify(id=_id)


class TriggerResourceView(APIView):
    url_prefix = "/triggers/resources"

    @validate_app
    @auth_with_app_token
    @args_required("resource_type_id")
    def post(self):
        app_id = request.values.get('app_id')
        resource_type_id = request.values.get('resource_type_id')
        wildcard = request.values.get('pattern')
        uid = request.values.get('owner')

        resources = TriggerCRUD.get_resources(app_id, resource_type_id, wildcard, uid)
        resources = [i.to_dict() for i in resources]

        return self.jsonify(resources)


class TriggerApplyView(APIView):
    url_prefix = "/triggers/<int:_id>/apply"

    @auth_only_for_acl
    def post(self, _id):
        TriggerCRUD.apply(_id)

        return self.jsonify(id=_id)


class TriggerCancelView(APIView):
    url_prefix = "/triggers/<int:_id>/cancel"

    @auth_only_for_acl
    def post(self, _id):
        TriggerCRUD.cancel(_id)

        return self.jsonify(id=_id)
