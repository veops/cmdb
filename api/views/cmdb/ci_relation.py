# -*- coding:utf-8 -*- 


from flask import request

from api.lib.cmdb.ci import CIRelationManager
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.resource import APIView


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
