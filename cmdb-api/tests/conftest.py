# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import jwt
import pytest
from webtest import TestApp
from flask import Response, json
from flask.testing import FlaskClient
from werkzeug.datastructures import Headers

from api.app import create_app
from api.extensions import db
from api.models.acl import User


class CMDBTestClient(FlaskClient):
    TEST_APP_SECRET = "test"

    def open(self, *args, **kwargs):
        headers = kwargs.pop("headers", Headers())
        headers.setdefault("User-Agent", "py.test")
        kwargs["headers"] = headers

        json_data = kwargs.pop("json")
        if json_data is not None:
            kwargs["data"] = json.dumps(json_data)
            if not kwargs.get("content_type"):
                kwargs["content_type"] = "application/json"

        auth = kwargs.pop("auth", (
            "Access-Token",
            jwt.encode({"sub": "test@xx.com"}, key=self.TEST_APP_SECRET)
        ))
        kwargs["headers"][auth[0]] = auth[1]

        return super(CMDBTestClient, self).open(*args, **kwargs)


class CMDBTestResponse(Response):
    @property
    def json(self):
        return json.loads(self.data)


@pytest.fixture(scope="session")
def app():
    """Create application for the tests."""
    _app = create_app("tests.settings")
    _app.config['SECRET_KEY'] = CMDBTestClient.TEST_APP_SECRET
    _app.test_client_class = CMDBTestClient
    _app.response_class = CMDBTestResponse
    ctx = _app.test_request_context()
    ctx.push()
    yield _app

    ctx.pop()


@pytest.fixture(scope="session")
def client(app):
    with app.test_client(use_cookies=False) as c:
        yield c


@pytest.fixture(scope="session")
def database(app):
    """Clean database after each case finished"""
    setup_db()
    yield db
    teardown_db()


@pytest.fixture(scope="function")
def session(database, app):
    with app.app_context():
        clean_db()
        yield database.session
        database.session.rollback()


def setup_db():
    teardown_db()
    db.create_all()
    # create test user


def teardown_db():
    db.session.remove()
    db.drop_all()
    db.session.bind.dispose()


def clean_db():
    """clean all data but not drop table"""
    for table in reversed(db.metadata.sorted_tables):
        if table.fullname in ["users"]:
            continue
        db.session.execute(table.delete())
        db.session.commit()

    if not User.get_by(email="test@xx.com"):
        print("hello world xxxxx")
        u = User.create(
            flush=True,
            username="test",
            nickname="测试",
            email="test@xx.com",
            key="",
            secret=""
        )
        u._set_password("123456")
        u.save()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)
