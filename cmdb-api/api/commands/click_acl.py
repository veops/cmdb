import click
from flask.cli import with_appcontext

from api.lib.perm.acl.user import UserCRUD


@click.command()
@with_appcontext
def init_acl():
    """
    acl init
    """
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


@click.command()
@with_appcontext
def add_user():
    """
    create a user

    is_admin: default is False

    """

    from api.models.acl import App
    from api.lib.perm.acl.cache import AppCache
    from api.lib.perm.acl.cache import RoleCache
    from api.lib.perm.acl.role import RoleCRUD
    from api.lib.perm.acl.role import RoleRelationCRUD

    username = click.prompt('Enter username', confirmation_prompt=False)
    password = click.prompt('Enter password', hide_input=True, confirmation_prompt=True)
    email = click.prompt('Enter email   ', confirmation_prompt=False)
    is_admin = click.prompt('Admin (Y/N)   ', confirmation_prompt=False, type=bool, default=False)

    UserCRUD.add(username=username, password=password, email=email)

    if is_admin:
        app = AppCache.get('acl') or App.create(name='acl')
        acl_admin = RoleCache.get('acl_admin') or RoleCRUD.add_role('acl_admin', app.id, True)
        rid = RoleCache.get_by_name(None, username).id

        RoleRelationCRUD.add(acl_admin, acl_admin.id, [rid], app.id)
