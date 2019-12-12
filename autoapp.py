# -*- coding: utf-8 -*-


from flask import g
from flask_login import current_user

from api.app import create_app

app = create_app()


@app.before_request
def before_request():
    g.user = current_user
