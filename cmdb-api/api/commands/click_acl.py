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

    username = click.prompt('Enter username', confirmation_prompt=False)
    password = click.prompt('Enter password', hide_input=True, confirmation_prompt=True)
    email = click.prompt('Enter email   ', confirmation_prompt=False)

    UserCRUD.add(username=username, password=password, email=email)
