# -*- coding:utf-8 -*- 


import time

from flask import abort
from flask import current_app
from flask import request

from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.search import SearchError
from api.lib.cmdb.search.ci_relation.search import Search
from api.lib.perm.auth import auth_abandoned
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.lib.utils import handle_arg_list
from api.resource import APIView


class CIRelationSearchView(APIView):
    url_prefix = ("/ci_relations/s", "/ci_relations/search")

    @auth_abandoned
    def get(self):
        """@params: q: query statement
                    fl: filter by column
                    count: the number of ci
                    root_id: ci id
                    level: default is 1
                    facet: statistic
        """

        page = get_page(request.values.get("page", 1))
        count = get_page_size(request.values.get("count") or request.values.get("page_size"))

        root_id = request.values.get('root_id')
        level = request.values.get('level', 1)

        query = request.values.get('q', "")
        fl = handle_arg_list(request.values.get('fl', ""))
        facet = handle_arg_list(request.values.get("facet", ""))
        sort = request.values.get("sort")

        start = time.time()
        s = Search(root_id, level, query, fl, facet, page, count, sort)
        try:
            response, counter, total, page, numfound, facet = s.search()
        except SearchError as e:
            return abort(400, str(e))
        current_app.logger.debug("search time is :{0}".format(time.time() - start))

        return self.jsonify(numfound=numfound,
                            total=total,
                            page=page,
                            facet=facet,
                            counter=counter,
                            result=response)


class CIRelationStatisticsView(APIView):
    url_prefix = "/ci_relations/statistics"

    @auth_abandoned
    def get(self):
        root_ids = list(map(int, handle_arg_list(request.values.get('root_ids'))))
        level = request.values.get('level', 1)

        start = time.time()
        s = Search(root_ids, level)
        try:
            result = s.statistics()
        except SearchError as e:
            return abort(400, str(e))
        current_app.logger.debug("search time is :{0}".format(time.time() - start))

        return self.jsonify(result)


class GetSecondCIsView(APIView):
    url_prefix = "/ci_relations/<int:first_ci_id>/second_cis"

    def get(self, first_ci_id):
        page = get_page(request.values.get("page", 1))
        count = get_page_size(request.values.get("count"))
        relation_type = request.values.get("relation_type", "contain")

        manager = CIRelationManager()
        numfound, total, second_cis = manager.get_second_cis(
            first_ci_id, page=page, per_page=count, relation_type=relation_type)

        return self.jsonify(numfound=numfound,
                            total=total,
                            page=page,
                            second_cis=second_cis)


class GetFirstCIsView(APIView):
    url_prefix = "/ci_relations/<int:second_ci_id>/first_cis"

    def get(self, second_ci_id):
        page = get_page(request.values.get("page", 1))
        count = get_page_size(request.values.get("count"))

        manager = CIRelationManager()
        numfound, total, first_cis = manager.get_first_cis(second_ci_id, per_page=count, page=page)

        return self.jsonify(numfound=numfound,
                            total=total,
                            page=page,
                            first_cis=first_cis)


class CIRelationView(APIView):
    url_prefix = "/ci_relations/<int:first_ci_id>/<int:second_ci_id>"

    def post(self, first_ci_id, second_ci_id):
        manager = CIRelationManager()
        res = manager.add(first_ci_id, second_ci_id)
        return self.jsonify(cr_id=res)

    def delete(self, first_ci_id, second_ci_id):
        manager = CIRelationManager()
        manager.delete_2(first_ci_id, second_ci_id)
        return self.jsonify(message="CIType Relation is deleted")


class DeleteCIRelationView(APIView):
    url_prefix = "/ci_relations/<int:cr_id>"

    def delete(self, cr_id):
        manager = CIRelationManager()
        manager.delete(cr_id)
        return self.jsonify(message="CIType Relation is deleted")
