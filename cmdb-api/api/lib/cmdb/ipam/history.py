# -*- coding:utf-8 -*-

from flask_login import current_user

from api.lib.cmdb.ipam.const import IPAddressBuiltinAttributes
from api.lib.mixin import DBMixin
from api.models.cmdb import IPAMOperationHistory
from api.models.cmdb import IPAMSubnetScan
from api.models.cmdb import IPAMSubnetScanHistory


class OperateHistoryManager(DBMixin):
    cls = IPAMOperationHistory

    def _can_add(self, **kwargs):
        kwargs['uid'] = current_user.uid

        return kwargs

    def _can_update(self, **kwargs):
        pass

    def _can_delete(self, **kwargs):
        pass


class ScanHistoryManager(DBMixin):
    cls = IPAMSubnetScanHistory

    def _can_add(self, **kwargs):
        return kwargs

    def add(self, **kwargs):
        kwargs.pop('_key', None)
        kwargs.pop('_secret', None)
        ci_id = kwargs.pop('ci_id', None)

        existed = self.cls.get_by(exec_id=kwargs['exec_id'], first=True, to_dict=False)
        if existed is None:
            self.cls.create(**kwargs)
        else:
            existed.update(**kwargs)

        if kwargs.get('ips'):
            from api.lib.cmdb.ipam.address import IpAddressManager
            IpAddressManager().assign_ips(kwargs['ips'], ci_id, kwargs.get('cidr'),
                                          **{IPAddressBuiltinAttributes.IS_USED: 1})

            scan_rule = IPAMSubnetScan.get_by(ci_id=ci_id, first=True, to_dict=False)
            if scan_rule is not None:
                scan_rule.update(last_scan_time=kwargs.get('start_at'))

        for i in self.cls.get_by(subnet_scan_id=kwargs.get('subnet_scan_id'), only_query=True).order_by(
                self.cls.id.desc()).offset(100):
            i.delete()

    def _can_update(self, **kwargs):
        pass

    def _can_delete(self, **kwargs):
        pass
