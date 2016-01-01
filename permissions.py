# -*- coding:utf-8 -*- 


from flask.ext.principal import RoleNeed, Permission


admin = Permission(RoleNeed('admin'))
auth = Permission(RoleNeed('authenticated'))
null = Permission(RoleNeed('null'))