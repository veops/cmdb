# -*- coding:utf-8 -*-

import ipaddress
from flask import abort

from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.const import BuiltinModelEnum
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.models.cmdb import CI
from api.models.cmdb import CIRelation
from api.models.cmdb import SubnetScan


class SubnetManager(object):
    def __init__(self):
        ci_type = CITypeCache.get(BuiltinModelEnum.IPAM_SUBNET)
        not ci_type and abort(400, ErrFormat.ipam_subnet_model_not_found.format(
            BuiltinModelEnum.IPAM_SUBNET))

        self.type_id = ci_type.id

    @staticmethod
    def _is_valid_cidr(cidr):
        try:
            ipaddress.ip_network(cidr)
        except ValueError:
            return abort(400, ErrFormat.ipam_cidr_invalid_notation.format(cidr))

    def _check_root_node_is_overlapping(self, cidr):
        none_root_nodes = [i.id for i in CI.get_by(only_query=True).join(
            CIRelation, CIRelation.second_ci_id == CI.id).filter(CI.type_id == self.type_id)]
        all_nodes = [i.id for i in CI.get_by(type_id=self.type_id, to_dict=False, fl=['id'])]

        root_nodes = set(all_nodes) - set(none_root_nodes)
        response, _, _, _, _, _ = SearchFromDB("_type:{}".format(self.type_id), ci_ids=list(root_nodes)).search()

        cur_subnet = ipaddress.ip_network(cidr)
        for item in response:
            if cur_subnet.overlaps(ipaddress.ip_network(item.get('cidr'))):
                return abort(400, ErrFormat.ipam_subnet_overlapped.format(cidr, item.get('cidr')))

    def _check_child_node_is_overlapping(self, parent_id, cidr):
        child_nodes = [i.second_ci_id for i in CIRelation.get_by(
            first_ci_id=parent_id, to_dict=False, fl=['second_ci_id'])]

        response, _, _, _, _, _ = SearchFromDB("_type:{}".format(self.type_id), ci_ids=list(child_nodes)).search()

        cur_subnet = ipaddress.ip_network(cidr)
        for item in response:
            if cur_subnet.overlaps(ipaddress.ip_network(item.get('cidr'))):
                return abort(400, ErrFormat.ipam_subnet_overlapped.format(cidr, item.get('cidr')))

    def validate_cidr(self, parent_id, cidr):
        self._is_valid_cidr(cidr)

        if not parent_id:
            return self._check_root_node_is_overlapping(cidr)

        parent_subnet = CIManager().get_ci_by_id(parent_id, need_children=False)
        if parent_subnet['ci_type'] == BuiltinModelEnum.IPAM_SUBNET:
            if parent_subnet.get('cidr'):
                prefix = int(cidr.split('/')[1])
                if int(parent_subnet['cidr'].split('/')[1]) >= prefix:
                    return abort(400, ErrFormat.ipam_subnet_prefix_length_invalid.format(prefix))

                valid_subnets = [str(i) for i in ipaddress.ip_network(parent_subnet['cidr']).subnets(new_prefix=prefix)]
                if cidr not in valid_subnets:
                    return abort(400, ErrFormat.ipam_cidr_invalid_subnet.format(cidr, valid_subnets))
            else:
                return abort(400, ErrFormat.ipam_parent_subnet_node_cidr_cannot_empty)

        self._check_child_node_is_overlapping(parent_id, cidr)

    def _add_cidr(self, cidr, **kwargs):
        return CIManager().add(self.type_id, cidr=cidr, **kwargs)

    @staticmethod
    def _add_scan_rule(ci_id, agent_id, cron, scan_enabled=True):
        SubnetScan.create(ci_id=ci_id, agent_id=agent_id, cron=cron, enabled=scan_enabled)

    @staticmethod
    def _add_relation(parent_id, child_id):
        if not parent_id or not child_id:
            return

        CIRelationManager().add(parent_id, child_id, valid=False)

    def add(self, cidr, parent_id, agent_id, cron, scan_enabled=True, **kwargs):
        self.validate_cidr(parent_id, cidr)

        ci_id = self._add_cidr(cidr, **kwargs)

        self._add_scan_rule(ci_id, agent_id, cron, scan_enabled)

        self._add_relation(parent_id, ci_id)

        return ci_id

    def update(self, _id, **kwargs):
        pass

    def delete(self, _id):
        pass
