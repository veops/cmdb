# -*- coding: utf-8 -*-
"""For debugging in ide"""

from tests.conftest import *
from pytest_mock import mocker
from _pytest.config import _prepareconfig

from tests.test_cmdb_attribute import test_create_attribute


for a in app():
    for d in database(a):
        for s in session(d, a):
            for c in client(a):
                for m in mocker(_prepareconfig()):
                    clean_db()
                    test_create_attribute(s, c)
