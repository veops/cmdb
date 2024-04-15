# -*- coding:utf-8 -*- 


import time

from flask import abort
from flask import current_app
from flask import request

from api.lib.cmdb.cache import RelationTypeCache
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search import SearchError
from api.lib.cmdb.search.ci_relation.search import Search
from api.lib.decorator import args_required
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.lib.utils import handle_arg_list
from api.resource import APIView


class CIRelationSearchView(APIView):
    url_prefix = ("/ci_relations/s", "/ci_relations/search")

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
        ancestor_ids = request.values.get('ancestor_ids') or None  # only for many to many
        root_parent_path = handle_arg_list(request.values.get('root_parent_path') or '')
        descendant_ids = list(map(int, handle_arg_list(request.values.get('descendant_ids', []))))
        level = list(map(int, handle_arg_list(request.values.get('level', '1'))))

        query = request.values.get('q', "")
        fl = handle_arg_list(request.values.get('fl', ""))
        facet = handle_arg_list(request.values.get("facet", ""))
        sort = request.values.get("sort")
        reverse = request.values.get("reverse") in current_app.config.get('BOOL_TRUE')
        has_m2m = request.values.get("has_m2m") in current_app.config.get('BOOL_TRUE')

        start = time.time()
        s = Search(root_id, level, query, fl, facet, page, count, sort, reverse,
                   ancestor_ids=ancestor_ids, has_m2m=has_m2m, root_parent_path=root_parent_path,
                   descendant_ids=descendant_ids)
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

    def get(self):
        root_ids = list(map(int, handle_arg_list(request.values.get('root_ids'))))
        level = request.values.get('level', 1)
        type_ids = set(map(int, handle_arg_list(request.values.get('type_ids', []))))
        ancestor_ids = request.values.get('ancestor_ids') or None  # only for many to many
        descendant_ids = list(map(int, handle_arg_list(request.values.get('descendant_ids', []))))
        has_m2m = request.values.get("has_m2m") in current_app.config.get('BOOL_TRUE')

        start = time.time()
        s = Search(root_ids, level, ancestor_ids=ancestor_ids, descendant_ids=descendant_ids, has_m2m=has_m2m)
        try:
            result = s.statistics(type_ids)
        except SearchError as e:
            return abort(400, str(e))
        current_app.logger.debug("search time is :{0}".format(time.time() - start))

        return self.jsonify(result)


class CIRelationSearchFullView(APIView):
    url_prefix = "/ci_relations/search/full"

    def get(self):
        root_ids = list(map(int, handle_arg_list(request.values.get('root_ids'))))
        level = request.values.get('level', 1)
        type_ids = list(map(int, handle_arg_list(request.values.get('type_ids', []))))
        has_m2m = request.values.get("has_m2m") in current_app.config.get('BOOL_TRUE')

        start = time.time()
        s = Search(root_ids, level, has_m2m=has_m2m)
        try:
            result = s.search_full(type_ids)
        except SearchError as e:
            return abort(400, str(e))
        current_app.logger.debug("search time is :{0}".format(time.time() - start))

        return self.jsonify(result)


class GetSecondCIsView(APIView):
    url_prefix = "/ci_relations/<int:first_ci_id>/second_cis"

    def get(self, first_ci_id):
        page = get_page(request.values.get("page", 1))
        count = get_page_size(request.values.get("count"))
        relation_type = request.values.get("relation_type")
        try:
            relation_type_id = RelationTypeCache.get(relation_type).id if relation_type else None
        except AttributeError:
            return abort(400, ErrFormat.invalid_relation_type.format(relation_type))

        manager = CIRelationManager()
        numfound, total, second_cis = manager.get_second_cis(
            first_ci_id, page=page, per_page=count, relation_type_id=relation_type_id)

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
        ancestor_ids = request.values.get('ancestor_ids') or None

        manager = CIRelationManager()
        res = manager.add(first_ci_id, second_ci_id, ancestor_ids=ancestor_ids)

        return self.jsonify(cr_id=res)

    def delete(self, first_ci_id, second_ci_id):
        ancestor_ids = request.values.get('ancestor_ids') or None

        manager = CIRelationManager()
        manager.delete_2(first_ci_id, second_ci_id, ancestor_ids=ancestor_ids)

        return self.jsonify(message="CIType Relation is deleted")


class DeleteCIRelationView(APIView):
    url_prefix = "/ci_relations/<int:cr_id>"

    def delete(self, cr_id):
        manager = CIRelationManager()
        manager.delete(cr_id)

        return self.jsonify(message="CIType Relation is deleted")


class BatchCreateOrUpdateCIRelationView(APIView):
    url_prefix = "/ci_relations/batch"

    @args_required('ci_ids')
    def post(self):
        ci_ids = list(map(int, request.values.get('ci_ids')))
        parents = list(map(int, request.values.get('parents', [])))
        children = list(map(int, request.values.get('children', [])))
        ancestor_ids = request.values.get('ancestor_ids') or None

        CIRelationManager.batch_update(ci_ids, parents, children, ancestor_ids=ancestor_ids)

        return self.jsonify(code=200)

    @args_required('ci_ids')
    @args_required('parents')
    def put(self):
        return self.post()

    @args_required('ci_ids')
    @args_required('parents')
    def delete(self):
        ci_ids = list(map(int, request.values.get('ci_ids')))
        parents = list(map(int, request.values.get('parents', [])))
        ancestor_ids = request.values.get('ancestor_ids') or None

        CIRelationManager.batch_delete(ci_ids, parents, ancestor_ids=ancestor_ids)

        return self.jsonify(code=200)
