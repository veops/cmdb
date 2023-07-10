# -*- coding:utf-8 -*-


from api.lib.cmdb.cache import CMDBCounterCache
from api.resource import APIView


class CMDBStatisticsView(APIView):
    url_prefix = "/statistics"

    def get(self):
        return self.jsonify(CMDBCounterCache.get())
