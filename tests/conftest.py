# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from api.app import create_app


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app("tests.settings")
    ctx = _app.test_request_context()
    ctx.push()
    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)
