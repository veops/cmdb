# -*- coding:utf-8 -*-

import redis_lock
from flask import abort

from api.extensions import rd
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.const import BuiltinModelEnum
from api.lib.cmdb.ipam.const import IPAddressAssignStatus
from api.lib.cmdb.ipam.const import IPAddressBuiltinAttributes
from api.lib.cmdb.ipam.const import OperateTypeEnum
from api.lib.cmdb.ipam.const import SubnetBuiltinAttributes
from api.lib.cmdb.ipam.history import OperateHistoryManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.lib.cmdb.search.ci_relation.search import Search as RelationSearch


class IpAddressManager(object):
    def __init__(self):
        self.ci_type = CITypeCache.get(BuiltinModelEnum.IPAM_ADDRESS) or abort(
            404, ErrFormat.ipam_address_model_not_found.format(BuiltinModelEnum.IPAM_ADDRESS))

        self.type_id = self.ci_type.id

    @staticmethod
    def list_ip_address(parent_id):
        numfound, _, result = CIRelationManager.get_second_cis(parent_id, per_page="all")

        return numfound, result

    def _get_cis(self, subnet_id, ips):

        q = "_type:{},{}:({})".format(self.type_id, IPAddressBuiltinAttributes.IP, ";".join(ips or []))

        response, _, _, _, _, _ = RelationSearch([subnet_id], level=[1], query=q, count=1000000).search()

        return response

    @staticmethod
    def _add_relation(parent_id, child_id):
        if not parent_id or not child_id:
            return

        CIRelationManager().add(parent_id, child_id, valid=False, apply_async=False)

    @staticmethod
    def calc_used_count(subnet_id):
        q = "{}:(0;2),-{}:true".format(IPAddressBuiltinAttributes.ASSIGN_STATUS, IPAddressBuiltinAttributes.IS_USED)

        return len(set(RelationSearch([subnet_id], level=[1], query=q, count=1000000).search(only_ids=True) or []))

    @staticmethod
    def _calc_assign_count(subnet_id):
        q = "{}:(0;2)".format(IPAddressBuiltinAttributes.ASSIGN_STATUS)

        return len(set(RelationSearch([subnet_id], level=[1], query=q, count=1000000).search(only_ids=True) or []))

    def _update_subnet_count(self, subnet_id, assign_count_computed, used_count=None):
        payload = {}

        cur = CIManager.get_ci_by_id(subnet_id, need_children=False)
        if assign_count_computed:
            payload[SubnetBuiltinAttributes.ASSIGN_COUNT] = self._calc_assign_count(subnet_id)
        if used_count is not None:
            payload[SubnetBuiltinAttributes.USED_COUNT] = used_count

        payload[SubnetBuiltinAttributes.FREE_COUNT] = (cur[SubnetBuiltinAttributes.HOSTS_COUNT] -
                                                       self.calc_used_count(subnet_id))
        CIManager().update(subnet_id, **payload)

    def assign_ips(self, ips, subnet_id, cidr, **kwargs):
        """

        :param ips: ip list
        :param subnet_id: subnet id
        :param cidr: subnet cidr
        :param kwargs: other attributes for ip address
        :return:
        """
        if subnet_id is not None:
            subnet = CIManager.get_ci_by_id(subnet_id)
        else:
            cis, _, _, _, _, _ = SearchFromDB("_type:{},{}:{}".format(
                BuiltinModelEnum.IPAM_SUBNET, SubnetBuiltinAttributes.CIDR, cidr),
                parent_node_perm_passed=True).search()
            if cis:
                subnet = cis[0]
                subnet_id = subnet['_id']
            else:
                return abort(400, ErrFormat.ipam_address_model_not_found)

        with (redis_lock.Lock(rd.r, "IPAM_ASSIGN_ADDRESS_{}".format(subnet_id),
                              expire=60, auto_renewal=True)):
            cis = self._get_cis(subnet_id, ips)
            ip2ci = {ci[IPAddressBuiltinAttributes.IP]: ci for ci in cis}

            ci_ids = []
            for ip in ips:
                kwargs['name'] = ip
                kwargs[IPAddressBuiltinAttributes.IP] = ip
                if ip not in ip2ci:
                    ci_id = CIManager.add(self.type_id, _sync=True, **kwargs)
                else:
                    ci_id = ip2ci[ip]['_id']
                    CIManager().update(ci_id, _sync=True, **kwargs)
                ci_ids.append(ci_id)

                self._add_relation(subnet_id, ci_id)

            if ips and IPAddressBuiltinAttributes.ASSIGN_STATUS in kwargs:
                self._update_subnet_count(subnet_id, True)

            if ips and IPAddressBuiltinAttributes.IS_USED in kwargs:
                q = "{}:true".format(IPAddressBuiltinAttributes.IS_USED)
                cur_used_ids = RelationSearch([subnet_id], level=[1], query=q).search(only_ids=True)
                for _id in set(cur_used_ids) - set(ci_ids):
                    CIManager().update(_id, **{IPAddressBuiltinAttributes.IS_USED: False})

                self._update_subnet_count(subnet_id, False, used_count=len(ips))

        if kwargs.get(IPAddressBuiltinAttributes.ASSIGN_STATUS) in (
                IPAddressAssignStatus.ASSIGNED, IPAddressAssignStatus.RESERVED):
            OperateHistoryManager().add(operate_type=OperateTypeEnum.ASSIGN_ADDRESS,
                                        cidr=subnet.get(SubnetBuiltinAttributes.CIDR),
                                        description=" | ".join(ips))

        elif kwargs.get(IPAddressBuiltinAttributes.ASSIGN_STATUS) == IPAddressAssignStatus.UNASSIGNED:
            OperateHistoryManager().add(operate_type=OperateTypeEnum.REVOKE_ADDRESS,
                                        cidr=subnet.get(SubnetBuiltinAttributes.CIDR),
                                        description=" | ".join(ips))
