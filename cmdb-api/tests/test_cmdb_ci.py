# -*- coding: utf-8 -*-


class TestCI:

    def test_ci_search_only_type_query(self, app):
        with app.test_client() as c:
            rv = c.get('/api/v0.1/ci/s?q=_type:server', json={})
            json_data = rv.get_json()
            assert type(json_data.get("result")) is list
