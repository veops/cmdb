# -*- coding:utf-8 -*- 


from flask import abort
from flask import current_app
from flask import request

from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.lib.utils import handle_arg_list
from api.resource import APIView


class AttributeSearchView(APIView):
    url_prefix = ("/attributes/s", "/attributes/search")

    def get(self):
        name = request.values.get("name")
        alias = request.values.get("alias")
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        numfound, res = AttributeManager.search_attributes(name=name, alias=alias, page=page, page_size=page_size)

        return self.jsonify(page=page,
                            page_size=page_size,
                            numfound=numfound,
                            total=len(res),
                            attributes=res)


class AttributeView(APIView):
    url_prefix = ("/attributes", "/attributes/<string:attr_name>", "/attributes/<int:attr_id>")

    def get(self, attr_name=None, attr_id=None):
        attr_manager = AttributeManager()
        attr_dict = None
        if attr_name is not None:
            attr_dict = attr_manager.get_attribute_by_name(attr_name)
            if attr_dict is None:
                attr_dict = attr_manager.get_attribute_by_alias(attr_name)

            if not attr_dict:
                return abort(404, ErrFormat.attribute_not_found.format("name={}".format(attr_name)))
        elif attr_id is not None:
            attr_dict = attr_manager.get_attribute_by_id(attr_id)

            if not attr_dict:
                return abort(404, ErrFormat.attribute_not_found.format("name={}".format(attr_name)))

        return self.jsonify(attribute=attr_dict)

    @args_required("name")
    @args_validate(AttributeManager.cls)
    def post(self):
        choice_value = handle_arg_list(request.values.get("choice_value"))
        params = request.values
        params["choice_value"] = choice_value

        current_app.logger.debug(params)

        attr_id = AttributeManager.add(**params)

        return self.jsonify(attr_id=attr_id)

    @args_validate(AttributeManager.cls)
    def put(self, attr_id):
        choice_value = handle_arg_list(request.values.get("choice_value"))
        params = request.values
        params["choice_value"] = choice_value
        current_app.logger.debug(params)
        AttributeManager().update(attr_id, **params)

        return self.jsonify(attr_id=attr_id)

    def delete(self, attr_id):
        attr_name = AttributeManager.delete(attr_id)

        return self.jsonify(message="attribute {0} deleted".format(attr_name))
