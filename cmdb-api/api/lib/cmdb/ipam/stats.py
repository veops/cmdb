# -*- coding:utf-8 -*-


import json
from flask import abort

from api.extensions import rd
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.const import BuiltinModelEnum
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.models.cmdb import CI
from api.models.cmdb import CIRelation
from api.models.cmdb import IPAMSubnetScan


class Stats(object):
    def __init__(self):
        self.address_type = CITypeCache.get(BuiltinModelEnum.IPAM_ADDRESS)
        not self.address_type and abort(400, ErrFormat.ipam_address_model_not_found.format(
            BuiltinModelEnum.IPAM_ADDRESS))

        self.address_type_id = self.address_type.id

        self.subnet_type = CITypeCache.get(BuiltinModelEnum.IPAM_SUBNET)
        not self.subnet_type and abort(400, ErrFormat.ipam_address_model_not_found.format(
            BuiltinModelEnum.IPAM_ADDRESS))

        self.subnet_type_id = self.subnet_type.id

    def leaf_nodes(self, parent_id):
        if str(parent_id) == '0':  # all
            ci_ids = [i.id for i in CI.get_by(type_id=self.subnet_type_id, to_dict=False)]
            has_children_ci_ids = [i.first_ci_id for i in CIRelation.get_by(
                only_query=True).join(CI, CIRelation.second_ci_id == CI.id).filter(
                CIRelation.first_ci_id.in_(ci_ids)).filter(CI.type_id == self.subnet_type_id)]

            return list(set(ci_ids) - set(has_children_ci_ids))

        else:
            type_id = CIManager().get_by_id(parent_id).type_id
            key = [(str(parent_id), type_id)]
            result = []
            while True:
                res = [json.loads(x).items() for x in [i or '{}' for i in rd.get(
                    [i[0] for i in key], REDIS_PREFIX_CI_RELATION) or []]]

                for idx, i in enumerate(res):
                    if (not i or list(i)[0][1] == self.address_type_id) and key[idx][1] == self.subnet_type_id:
                        result.append(int(key[idx][0]))

                res = [j for i in res for j in i]  # [(id, type_id)]

                if not res:
                    return result

                key = res

    def statistic_subnets(self, subnet_ids):
        if subnet_ids:
            response, _, _, _, _, _ = SearchFromDB(
                "_type:{}".format(self.subnet_type_id),
                ci_ids=subnet_ids,
                count=1000000,
                parent_node_perm_passed=True,
            ).search()
        else:
            response = []

        scans = IPAMSubnetScan.get_by(only_query=True).filter(IPAMSubnetScan.ci_id.in_(list(map(int, subnet_ids))))
        id2scan = {i.ci_id: i for i in scans}

        address_num, address_free_num, address_assign_num, address_used_num = 0, 0, 0, 0
        for subnet in response:
            address_num += (subnet.get('hosts_count') or 0)
            address_free_num += (subnet.get('free_count') or 0)
            address_assign_num += (subnet.get('assign_count') or 0)
            address_used_num += (subnet.get('used_count') or 0)

            if id2scan.get(subnet['_id']):
                subnet['scan_enabled'] = id2scan[subnet['_id']].scan_enabled
                subnet['last_scan_time'] = id2scan[subnet['_id']].last_scan_time
            else:
                subnet['scan_enabled'] = False
                subnet['last_scan_time'] = None

        return response, address_num, address_free_num, address_assign_num, address_used_num

    def summary(self, parent_id):
        subnet_ids = self.leaf_nodes(parent_id)

        subnets, address_num, address_free_num, address_assign_num, address_used_num = (
            self.statistic_subnets(subnet_ids))

        return dict(subnet_num=len(subnets),
                    address_num=address_num,
                    address_free_num=address_free_num,
                    address_assign_num=address_assign_num,
                    address_unassign_num=address_num - address_assign_num,
                    address_used_num=address_used_num,
                    address_used_free_num=address_num - address_used_num,
                    subnets=subnets)
