# -*- coding:utf-8 -*-

from collections import defaultdict

import ipaddress
from flask import abort

from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.const import BuiltinModelEnum, BUILTIN_ATTRIBUTES
from api.lib.cmdb.ipam.const import OperateTypeEnum
from api.lib.cmdb.ipam.const import SubnetBuiltinAttributes
from api.lib.cmdb.ipam.history import OperateHistoryManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.models.cmdb import CI
from api.models.cmdb import CIRelation
from api.models.cmdb import IPAMSubnetScan


class SubnetManager(object):
    def __init__(self):
        self.ci_type = CITypeCache.get(BuiltinModelEnum.IPAM_SUBNET)
        not self.ci_type and abort(400, ErrFormat.ipam_subnet_model_not_found.format(
            BuiltinModelEnum.IPAM_SUBNET))

        self.type_id = self.ci_type.id

    def scan_rules(self, oneagent_id, last_update_at=None):
        result = []
        rules = IPAMSubnetScan.get_by(agent_id=oneagent_id, to_dict=True)
        ci_ids = [i['ci_id'] for i in rules]
        if ci_ids:
            response, _, _, _, _, _ = SearchFromDB("_type:{}".format(self.type_id),
                                                   ci_ids=list(ci_ids),
                                                   count=1000000,
                                                   fl=[SubnetBuiltinAttributes.CIDR],
                                                   parent_node_perm_passed=True).search()
            id2ci = {i['_id']: i for i in response}

            for rule in rules:
                if rule['ci_id'] in id2ci:
                    rule[SubnetBuiltinAttributes.CIDR] = id2ci[rule['ci_id']][SubnetBuiltinAttributes.CIDR]
                    result.append(rule)

        new_last_update_at = ""
        for i in result:
            __last_update_at = max([i['updated_at'] or "", i['created_at'] or ""])
            if new_last_update_at < __last_update_at:
                new_last_update_at = __last_update_at

        if not last_update_at or new_last_update_at > last_update_at:
            return result, new_last_update_at
        else:
            return [], new_last_update_at

    @staticmethod
    def get_hosts(cidr):
        try:
            return list(map(str, ipaddress.ip_network(cidr).hosts()))
        except ValueError:
            return []

    def get_by_id(self, subnet_id):
        response, _, _, _, _, _ = SearchFromDB("_type:{}".format(self.type_id),
                                               ci_ids=[subnet_id],
                                               parent_node_perm_passed=True).search()
        scan_rule = IPAMSubnetScan.get_by(ci_id=subnet_id, first=True, to_dict=True)
        if scan_rule and response:
            scan_rule.update(response[0])

        return scan_rule

    def tree_view(self):
        scope = CITypeCache.get(BuiltinModelEnum.IPAM_SCOPE)
        ci_types = scope and [scope.id, self.type_id] or [self.type_id]

        relations = defaultdict(set)
        ids = set()
        has_parent_ids = set()
        for i in CIRelation.get_by(only_query=True).join(
                CI, CI.id == CIRelation.first_ci_id).filter(CI.type_id.in_(ci_types)):
            relations[i.first_ci_id].add(i.second_ci_id)
            ids.add(i.first_ci_id)
            ids.add(i.second_ci_id)
            has_parent_ids.add(i.second_ci_id)
        for i in CIRelation.get_by(only_query=True).join(
                CI, CI.id == CIRelation.second_ci_id).filter(CI.type_id.in_(ci_types)):
            relations[i.first_ci_id].add(i.second_ci_id)
            ids.add(i.first_ci_id)
            ids.add(i.second_ci_id)
            has_parent_ids.add(i.second_ci_id)

        for i in CI.get_by(only_query=True).filter(CI.type_id.in_(ci_types)):
            ids.add(i.id)

        for _id in ids:
            if _id not in has_parent_ids:
                relations[None].add(_id)

        type2name = dict()
        type2name[self.type_id] = AttributeCache.get(self.ci_type.show_id or self.ci_type.unique_id).name

        fl = [type2name[self.type_id]]
        if scope:
            type2name[scope.id] = AttributeCache.get(scope.show_id or scope.unique_id).name
            fl.append(type2name[scope.id])

        response, _, _, _, _, _ = SearchFromDB("_type:({})".format(";".join(map(str, ci_types))),
                                               ci_ids=list(ids),
                                               count=1000000,
                                               fl=list(set(fl + [SubnetBuiltinAttributes.CIDR])),
                                               parent_node_perm_passed=True).search()
        id2ci = {i['_id']: i for i in response}

        def _build_tree(_tree, parent_id=None):
            tree = []
            for child_id in _tree.get(parent_id, []):
                children = sorted(_build_tree(_tree, child_id), key=lambda x: x['_id'])
                if not id2ci.get(child_id):
                    continue
                tree.append({'children': children, **id2ci[child_id]})
            return tree

        result = sorted(_build_tree(relations), key=lambda x: x['_id'])

        return result, type2name

    @staticmethod
    def _is_valid_cidr(cidr):
        try:
            return str(ipaddress.ip_network(cidr))
        except ValueError:
            return abort(400, ErrFormat.ipam_cidr_invalid_notation.format(cidr))

    def _check_root_node_is_overlapping(self, cidr, _id=None):
        none_root_nodes = [i.id for i in CI.get_by(only_query=True).join(
            CIRelation, CIRelation.second_ci_id == CI.id).filter(CI.type_id == self.type_id)]
        all_nodes = [i.id for i in CI.get_by(type_id=self.type_id, to_dict=False, fl=['id'])]

        root_nodes = set(all_nodes) - set(none_root_nodes) - set(_id and [_id] or [])
        response, _, _, _, _, _ = SearchFromDB("_type:{}".format(self.type_id),
                                               ci_ids=list(root_nodes),
                                               parent_node_perm_passed=True).search()

        cur_subnet = ipaddress.ip_network(cidr)
        for item in response:
            if item['_id'] == _id:
                continue

            if cur_subnet.overlaps(ipaddress.ip_network(item.get(SubnetBuiltinAttributes.CIDR))):
                return abort(400, ErrFormat.ipam_subnet_overlapped.format(cidr, item.get(SubnetBuiltinAttributes.CIDR)))

        return cidr

    def _check_child_node_is_overlapping(self, parent_id, cidr, _id=None):
        child_nodes = [i.second_ci_id for i in CIRelation.get_by(
            first_ci_id=parent_id, to_dict=False, fl=['second_ci_id']) if i.second_ci_id != _id]
        if not child_nodes:
            return

        response, _, _, _, _, _ = SearchFromDB("_type:{}".format(self.type_id),
                                               ci_ids=list(child_nodes),
                                               parent_node_perm_passed=True).search()

        cur_subnet = ipaddress.ip_network(cidr)
        for item in response:
            if item['_id'] == _id:
                continue

            if cur_subnet.overlaps(ipaddress.ip_network(item.get(SubnetBuiltinAttributes.CIDR))):
                return abort(400, ErrFormat.ipam_subnet_overlapped.format(cidr, item.get(SubnetBuiltinAttributes.CIDR)))

    def validate_cidr(self, parent_id, cidr, _id=None):
        cidr = self._is_valid_cidr(cidr)

        if not parent_id:
            return self._check_root_node_is_overlapping(cidr, _id)

        parent_subnet = CIManager().get_ci_by_id(parent_id, need_children=False)
        if parent_subnet['ci_type'] == BuiltinModelEnum.IPAM_SUBNET:
            if parent_subnet.get(SubnetBuiltinAttributes.CIDR):
                prefix = int(cidr.split('/')[1])
                if int(parent_subnet[SubnetBuiltinAttributes.CIDR].split('/')[1]) >= prefix:
                    return abort(400, ErrFormat.ipam_subnet_prefix_length_invalid.format(prefix))

                valid_subnets = [str(i) for i in
                                 ipaddress.ip_network(parent_subnet[SubnetBuiltinAttributes.CIDR]).subnets(
                                     new_prefix=prefix)]
                if cidr not in valid_subnets:
                    return abort(400, ErrFormat.ipam_cidr_invalid_subnet.format(cidr, valid_subnets))
            else:
                return abort(400, ErrFormat.ipam_parent_subnet_node_cidr_cannot_empty)

        self._check_child_node_is_overlapping(parent_id, cidr, _id)

        return cidr

    def _add_subnet(self, cidr, **kwargs):
        kwargs[SubnetBuiltinAttributes.HOSTS_COUNT] = ipaddress.ip_network(cidr).num_addresses - 2
        kwargs[SubnetBuiltinAttributes.USED_COUNT] = 0
        kwargs[SubnetBuiltinAttributes.ASSIGN_COUNT] = 0
        kwargs[SubnetBuiltinAttributes.FREE_COUNT] = kwargs[SubnetBuiltinAttributes.HOSTS_COUNT]

        return CIManager().add(self.type_id, cidr=cidr, **kwargs)

    @staticmethod
    def _add_scan_rule(ci_id, agent_id, cron, scan_enabled=True):
        IPAMSubnetScan.create(ci_id=ci_id, agent_id=agent_id, cron=cron, scan_enabled=scan_enabled)

    @staticmethod
    def _add_relation(parent_id, child_id):
        if not parent_id or not child_id:
            return

        CIRelationManager().add(parent_id, child_id, valid=False)

    def add(self, cidr, parent_id, agent_id, cron, scan_enabled=True, **kwargs):
        cidr = self.validate_cidr(parent_id, cidr)

        ci_id = self._add_subnet(cidr, **kwargs)

        self._add_scan_rule(ci_id, agent_id, cron, scan_enabled)

        self._add_relation(parent_id, ci_id)

        OperateHistoryManager().add(operate_type=OperateTypeEnum.ADD_SUBNET,
                                    cidr=cidr,
                                    description=cidr)

        return ci_id

    @staticmethod
    def _update_subnet(_id, **kwargs):
        return CIManager().update(_id, **kwargs)

    @staticmethod
    def _update_scan_rule(ci_id, agent_id, cron, scan_enabled=True):
        existed = IPAMSubnetScan.get_by(ci_id=ci_id, first=True, to_dict=False)
        if existed is not None:
            existed.update(ci_id=ci_id, agent_id=agent_id, cron=cron, scan_enabled=scan_enabled)
        else:
            IPAMSubnetScan.create(ci_id=ci_id, agent_id=agent_id, cron=cron, scan_enabled=scan_enabled)

    def update(self, _id, **kwargs):
        kwargs[SubnetBuiltinAttributes.CIDR] = self.validate_cidr(kwargs.pop('parent_id', None),
                                                                  kwargs.get(SubnetBuiltinAttributes.CIDR), _id)

        agent_id = kwargs.pop('agent_id', None)
        cron = kwargs.pop('cron', None)
        scan_enabled = kwargs.pop('scan_enabled', True)

        cur = CIManager.get_ci_by_id(_id, need_children=False)

        self._update_subnet(_id, **kwargs)

        self._update_scan_rule(_id, agent_id, cron, scan_enabled)

        OperateHistoryManager().add(operate_type=OperateTypeEnum.UPDATE_SUBNET,
                                    cidr=cur.get(SubnetBuiltinAttributes.CIDR),
                                    description="{} -> {}".format(cur.get(SubnetBuiltinAttributes.CIDR),
                                                                  kwargs.get(SubnetBuiltinAttributes.CIDR)))

        return _id

    @classmethod
    def delete(cls, _id):
        if CIRelation.get_by(only_query=True).filter(CIRelation.first_ci_id == _id).first():
            return abort(400, ErrFormat.ipam_subnet_cannot_delete)

        existed = IPAMSubnetScan.get_by(ci_id=_id, first=True, to_dict=False)
        existed and existed.delete()

        for i in CIRelation.get_by(first_ci_id=_id, to_dict=False):
            i.delete()

        cur = CIManager.get_ci_by_id(_id, need_children=False)

        CIManager().delete(_id)

        OperateHistoryManager().add(operate_type=OperateTypeEnum.DELETE_SUBNET,
                                    cidr=cur.get(SubnetBuiltinAttributes.CIDR),
                                    description=cur.get(SubnetBuiltinAttributes.CIDR))

        return _id


class SubnetScopeManager(object):
    def __init__(self):
        self.ci_type = CITypeCache.get(BuiltinModelEnum.IPAM_SCOPE)
        not self.ci_type and abort(400, ErrFormat.ipam_subnet_model_not_found.format(
            BuiltinModelEnum.IPAM_SCOPE))

        self.type_id = self.ci_type.id

    def _add_scope(self, name):
        return CIManager().add(self.type_id, name=name)

    @staticmethod
    def _add_relation(parent_id, child_id):
        if not parent_id or not child_id:
            return

        CIRelationManager().add(parent_id, child_id, valid=False)

    def add(self, parent_id, name):
        ci_id = self._add_scope(name)

        self._add_relation(parent_id, ci_id)

        OperateHistoryManager().add(operate_type=OperateTypeEnum.ADD_SCOPE,
                                    description=name)

        return ci_id

    @staticmethod
    def _update_scope(_id, name):
        return CIManager().update(_id, name=name)

    def update(self, _id, name):
        cur = CIManager.get_ci_by_id(_id, need_children=False)

        res = self._update_scope(_id, name)

        OperateHistoryManager().add(operate_type=OperateTypeEnum.UPDATE_SCOPE,
                                    description="{} -> {}".format(cur.get('name'), name))

        return res

    @staticmethod
    def delete(_id):
        if CIRelation.get_by(first_ci_id=_id, first=True, to_dict=False):
            return abort(400, ErrFormat.ipam_scope_cannot_delete)

        cur = CIManager.get_ci_by_id(_id, need_children=False)

        CIManager().delete(_id)

        OperateHistoryManager().add(operate_type=OperateTypeEnum.DELETE_SCOPE,
                                    description=cur.get('name'))

        return _id
