# -*- coding:utf-8 -*-
import copy
import json
import uuid
from flask import abort
from flask import current_app
from flask import request
from flask_login import current_user
from io import BytesIO

from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryCICRUD
from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryCITypeCRUD
from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryCITypeRelationCRUD
from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryComponentsManager
from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryCounterCRUD
from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryExecHistoryCRUD
from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryHTTPManager
from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryRuleCRUD
from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryRuleSyncHistoryCRUD
from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoverySNMPManager
from api.lib.cmdb.auto_discovery.const import DEFAULT_INNER
from api.lib.cmdb.auto_discovery.const import PRIVILEGED_USERS
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search import SearchError
from api.lib.cmdb.search.ci import search as ci_search
from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl.acl import has_perm_from_args
from api.lib.utils import AESCrypto
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.lib.utils import handle_arg_list
from api.resource import APIView


class AutoDiscoveryRuleView(APIView):
    url_prefix = ("/adr", "/adr/<int:adr_id>")

    def get(self):
        _, res = AutoDiscoveryRuleCRUD.search(page=1, page_size=100000, **request.values)

        rebuild = False
        exists = {i['name'] for i in res}
        for i in copy.deepcopy(DEFAULT_INNER):
            if i['name'] not in exists:
                i.pop('en', None)
                AutoDiscoveryRuleCRUD().add(**i)
                rebuild = True

        if rebuild:
            _, res = AutoDiscoveryRuleCRUD.search(page=1, page_size=100000, **request.values)

        for i in res:
            if i['type'] == 'http':
                i['resources'] = AutoDiscoveryHTTPManager().get_resources(i['name'])

        return self.jsonify(res)

    @args_required("name", value_required=True)
    @args_validate(AutoDiscoveryRuleCRUD.cls)
    def post(self):
        return self.jsonify(AutoDiscoveryRuleCRUD().add(**request.values).to_dict())

    @args_validate(AutoDiscoveryRuleCRUD.cls)
    def put(self, adr_id):
        return self.jsonify(AutoDiscoveryRuleCRUD().update(adr_id, **request.values).to_dict())

    def delete(self, adr_id):
        AutoDiscoveryRuleCRUD().delete(adr_id)

        return self.jsonify(adr_id=adr_id)


class AutoDiscoveryRuleTemplateFileView(APIView):
    url_prefix = ("/adr/template/import/file", "/adr/template/export/file")

    def get(self):  # export
        adr_tpt = AutoDiscoveryRuleCRUD().get_by_inner()
        adr_tpt = dict(auto_discovery_rules=adr_tpt)

        bf = BytesIO()
        bf.write(bytes(json.dumps(adr_tpt).encode('utf-8')))
        bf.seek(0)

        return self.send_file(bf,
                              as_attachment=True,
                              download_name="cmdb_auto_discovery.json",
                              mimetype='application/json',
                              max_age=0)

    def post(self):
        f = request.files.get('file')

        if f is None:
            return abort(400, ErrFormat.argument_file_not_found)

        content = f.read()
        try:
            content = json.loads(content)
        except:
            return abort(400, ErrFormat.invalid_json)
        tpt = content.get('auto_discovery_rules')

        AutoDiscoveryRuleCRUD().import_template(tpt)

        return self.jsonify(code=200)


class AutoDiscoveryRuleHTTPView(APIView):
    url_prefix = ("/adr/http/<string:name>/categories",
                  "/adr/http/<string:name>/attributes",
                  "/adr/snmp/<string:name>/attributes",
                  "/adr/components/<string:name>/attributes",)

    def get(self, name):
        if "snmp" in request.url:
            return self.jsonify(AutoDiscoverySNMPManager.get_attributes())

        if "components" in request.url:
            return self.jsonify(AutoDiscoveryComponentsManager.get_attributes(name))

        if "attributes" in request.url:
            resource = request.values.get('resource')
            return self.jsonify(AutoDiscoveryHTTPManager.get_attributes(name, resource))

        return self.jsonify(AutoDiscoveryHTTPManager.get_categories(name))


class AutoDiscoveryCITypeView(APIView):
    url_prefix = ("/adt/ci_types/<int:type_id>",
                  "/adt/ci_types/<int:type_id>/attributes",
                  "/adt/<int:adt_id>")

    def get(self, type_id):
        if "attributes" in request.url:
            return self.jsonify(AutoDiscoveryCITypeCRUD.get_ad_attributes(type_id))

        _, res = AutoDiscoveryCITypeCRUD.search(page=1, page_size=100000, type_id=type_id, **request.values)
        for i in res:
            if isinstance(i.get("extra_option"), dict) and i['extra_option'].get('secret'):
                if not (current_user.username == "cmdb_agent" or current_user.uid == i['uid']):
                    i['extra_option'].pop('secret', None)
                else:
                    i['extra_option']['secret'] = AESCrypto.decrypt(i['extra_option']['secret'])

        return self.jsonify(res)

    @args_validate(AutoDiscoveryCITypeCRUD.cls)
    def post(self, type_id):
        if not request.values.get('interval'):
            request.values.pop('interval', None)

        return self.jsonify(AutoDiscoveryCITypeCRUD().add(type_id=type_id, **request.values).to_dict())

    @args_validate(AutoDiscoveryCITypeCRUD.cls)
    def put(self, adt_id):
        if not request.values.get('interval'):
            request.values.pop('interval', None)

        return self.jsonify(AutoDiscoveryCITypeCRUD().update(adt_id, **request.values).to_dict())

    def delete(self, adt_id):
        AutoDiscoveryCITypeCRUD().delete(adt_id)

        return self.jsonify(adt_id=adt_id)


class AutoDiscoveryCITypeRelationView(APIView):
    url_prefix = ("/adt/ci_types/<int:type_id>/relations", "/adt/relations/<int:_id>")

    def get(self, type_id):
        _, res = AutoDiscoveryCITypeRelationCRUD.search(page=1, page_size=100000, ad_type_id=type_id, **request.values)

        return self.jsonify(res)

    @args_required("relations")
    def post(self, type_id):
        return self.jsonify(AutoDiscoveryCITypeRelationCRUD().upsert(type_id, request.values['relations']))

    def put(self):
        return self.post()

    def delete(self, _id):
        AutoDiscoveryCITypeRelationCRUD().delete(_id)

        return self.jsonify(id=_id)


class AutoDiscoveryCIView(APIView):
    url_prefix = ("/adc", "/adc/<int:adc_id>", "/adc/ci_types/<int:type_id>/attributes", "/adc/ci_types")

    def get(self, type_id=None):
        if "attributes" in request.url:
            return self.jsonify(AutoDiscoveryCICRUD.get_attributes_by_type_id(type_id))
        elif "ci_types" in request.url:
            need_other = request.values.get("need_other")
            return self.jsonify(AutoDiscoveryCICRUD.get_ci_types(need_other))

        page = get_page(request.values.pop('page', 1))
        page_size = get_page_size(request.values.pop('page_size', None))
        fl = handle_arg_list(request.values.get('fl'))
        numfound, res = AutoDiscoveryCICRUD.search(page=page, page_size=page_size, fl=fl, **request.values)

        return self.jsonify(page=page,
                            page_size=page_size,
                            numfound=numfound,
                            total=len(res),
                            result=res)

    @args_validate(AutoDiscoveryCICRUD.cls)
    @args_required("type_id")
    @args_required("adt_id")
    @args_required("instance")
    def post(self):
        request.values.pop("_key", None)
        request.values.pop("_secret", None)

        return self.jsonify(AutoDiscoveryCICRUD().upsert(**request.values).to_dict())

    def put(self):
        return self.post()

    @has_perm_from_args("adc_id", ResourceTypeEnum.CI, PermEnum.DELETE, AutoDiscoveryCICRUD.get_type_name)
    def delete(self, adc_id):
        AutoDiscoveryCICRUD().delete(adc_id)

        return self.jsonify(adc_id=adc_id)


class AutoDiscoveryCIDelete2View(APIView):
    url_prefix = ("/adc",)

    def delete(self):
        type_id = request.values.get('type_id')
        unique_value = request.values.get('unique_value')

        AutoDiscoveryCICRUD.delete2(type_id, unique_value)

        return self.jsonify(type_id=type_id, unique_value=unique_value)


class AutoDiscoveryCIAcceptView(APIView):
    url_prefix = ("/adc/<int:adc_id>/accept",)

    @has_perm_from_args("adc_id", ResourceTypeEnum.CI, PermEnum.ADD, AutoDiscoveryCICRUD.get_type_name)
    def put(self, adc_id):
        AutoDiscoveryCICRUD.accept(None, adc_id=adc_id)

        return self.jsonify(adc_id=adc_id)


class AutoDiscoveryRuleSyncView(APIView):
    url_prefix = ("/adt/sync",)

    def get(self):
        if current_user.username not in PRIVILEGED_USERS:
            return abort(403)

        oneagent_name = request.values.get('oneagent_name')
        oneagent_id = request.values.get('oneagent_id')
        last_update_at = request.values.get('last_update_at')

        query = "oneagent_id:{}".format(oneagent_id)
        s = ci_search(query)
        try:
            response, _, _, _, _, _ = s.search()
        except SearchError as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            return abort(400, str(e))

        for res in response:
            if res.get('{}_name'.format(res['ci_type'])) == oneagent_name or oneagent_name == res.get('oneagent_name'):
                ci_id = res["_id"]
                rules, last_update_at = AutoDiscoveryCITypeCRUD.get(ci_id, oneagent_id, oneagent_name, last_update_at)

                return self.jsonify(rules=rules, last_update_at=last_update_at)

        rules, last_update_at = AutoDiscoveryCITypeCRUD.get(None, oneagent_id, oneagent_name, last_update_at)

        return self.jsonify(rules=rules, last_update_at=last_update_at)


class AutoDiscoveryRuleSyncHistoryView(APIView):
    url_prefix = ("/adt/<int:adt_id>/sync/histories",)

    def get(self, adt_id):
        page = get_page(request.values.pop('page', 1))
        page_size = get_page_size(request.values.pop('page_size', None))
        numfound, res = AutoDiscoveryRuleSyncHistoryCRUD.search(page=page,
                                                                page_size=page_size,
                                                                adt_id=adt_id,
                                                                **request.values)

        return self.jsonify(page=page,
                            page_size=page_size,
                            numfound=numfound,
                            total=len(res),
                            result=res)


class AutoDiscoveryTestView(APIView):
    url_prefix = ("/adt/<int:adt_id>/test", "/adt/test/<string:exec_id>/result")

    def get(self, exec_id):
        return self.jsonify(stdout="1\n2\n3", exec_id=exec_id)

    def post(self, adt_id):
        return self.jsonify(exec_id=uuid.uuid4().hex)


class AutoDiscoveryExecHistoryView(APIView):
    url_prefix = ("/adc/exec/histories",)

    @args_required('type_id')
    def get(self):
        page = get_page(request.values.pop('page', 1))
        page_size = get_page_size(request.values.pop('page_size', None))
        numfound, res = AutoDiscoveryExecHistoryCRUD.search(page=page,
                                                            page_size=page_size,
                                                            **request.values)

        return self.jsonify(page=page,
                            page_size=page_size,
                            numfound=numfound,
                            total=len(res),
                            result=res)

    @args_required('type_id')
    @args_required('stdout')
    def post(self):
        AutoDiscoveryExecHistoryCRUD().add(type_id=request.values.get('type_id'),
                                           stdout=request.values.get('stdout'))

        return self.jsonify(code=200)


class AutoDiscoveryCounterView(APIView):
    url_prefix = ("/adc/counter",)

    @args_required('type_id')
    def get(self):
        type_id = request.values.get('type_id')

        return self.jsonify(AutoDiscoveryCounterCRUD().get(type_id))
