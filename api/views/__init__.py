# -*- coding:utf-8 -*-

import os

from flask import Blueprint
from flask_restful import Api

from api.resource import register_resources
from .permission import GetResourcesView, HasPermissionView, GetUserInfoView
from .account import LoginView, LogoutView

HERE = os.path.abspath(os.path.dirname(__file__))

# account
blueprint_account = Blueprint('account_api', __name__, url_prefix='/api')
account_rest = Api(blueprint_account)
account_rest.add_resource(LoginView, LoginView.url_prefix)
account_rest.add_resource(LogoutView, LogoutView.url_prefix)

# permission
blueprint_perm_v01 = Blueprint('permission_api', __name__, url_prefix='/api/v1/perms')
perm_rest = Api(blueprint_perm_v01)
perm_rest.add_resource(GetResourcesView, GetResourcesView.url_prefix)
perm_rest.add_resource(HasPermissionView, HasPermissionView.url_prefix)
perm_rest.add_resource(GetUserInfoView, GetUserInfoView.url_prefix)


# cmdb
blueprint_cmdb_v01 = Blueprint('cmdb_api_v01', __name__, url_prefix='/api/v0.1')
rest = Api(blueprint_cmdb_v01)
register_resources(os.path.join(HERE, "cmdb"), rest)


# acl
blueprint_acl_v1 = Blueprint('acl_api_v1', __name__, url_prefix='/api/v1/acl')
rest = Api(blueprint_acl_v1)
register_resources(os.path.join(HERE, "acl"), rest)
