import click
from flask.cli import with_appcontext


@click.command()
@with_appcontext
def init_acl():
    from api.models.acl import Role
    from api.models.acl import App
    from api.tasks.acl import role_rebuild
    from api.lib.perm.acl.const import ACL_QUEUE

    roles = Role.get_by(to_dict=False)
    apps = App.get_by(to_dict=False)
    for role in roles:
        if role.app_id:
            role_rebuild.apply_async(args=(role.id, role.app_id), queue=ACL_QUEUE)
        else:
            for app in apps:
                role_rebuild.apply_async(args=(role.id, app.id), queue=ACL_QUEUE)


# @click.command()
# @with_appcontext
# def acl_clean():
#     from api.models.acl import Resource
#     from api.models.acl import Permission
#     from api.models.acl import RolePermission
#
#     perms = RolePermission.get_by(to_dict=False)
#
#     for r in perms:
#         perm = Permission.get_by_id(r.perm_id)
#         if perm and perm.app_id != r.app_id:
#             resource_id = r.resource_id
#             resource = Resource.get_by_id(resource_id)
#             perm_name = perm.name
#             existed = Permission.get_by(resource_type_id=resource.resource_type_id, name=perm_name, first=True,
#                                         to_dict=False)
#             if existed is not None:
#                 other = RolePermission.get_by(rid=r.rid, perm_id=existed.id, resource_id=resource_id)
#                 if not other:
#                     r.update(perm_id=existed.id)
#                 else:
#                     r.soft_delete()
#             else:
#                 r.soft_delete()
#
#
# @click.command()
# @with_appcontext
# def acl_has_resource_role():
#     from api.models.acl import Role
#     from api.models.acl import App
#     from api.lib.perm.acl.cache import HasResourceRoleCache
#     from api.lib.perm.acl.role import RoleCRUD
#
#     roles = Role.get_by(to_dict=False)
#     apps = App.get_by(to_dict=False)
#     for role in roles:
#         if role.app_id:
#             res = RoleCRUD.recursive_resources(role.id, role.app_id)
#             if res.get('resources') or res.get('groups'):
#                 HasResourceRoleCache.add(role.id, role.app_id)
#         else:
#             for app in apps:
#                 res = RoleCRUD.recursive_resources(role.id, app.id)
#                 if res.get('resources') or res.get('groups'):
#                     HasResourceRoleCache.add(role.id, app.id)
