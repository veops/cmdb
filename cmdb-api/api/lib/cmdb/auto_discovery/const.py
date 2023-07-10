# -*- coding:utf-8 -*-

from api.lib.cmdb.const import AutoDiscoveryType

DEFAULT_HTTP = [
    dict(name="阿里云", type=AutoDiscoveryType.HTTP, is_inner=True, is_plugin=False,
         option={'icon': {'name': 'caise-aliyun'}}),
    dict(name="腾讯云", type=AutoDiscoveryType.HTTP, is_inner=True, is_plugin=False,
         option={'icon': {'name': 'caise-tengxunyun'}}),
    dict(name="华为云", type=AutoDiscoveryType.HTTP, is_inner=True, is_plugin=False,
         option={'icon': {'name': 'caise-huaweiyun'}}),
    dict(name="AWS", type=AutoDiscoveryType.HTTP, is_inner=True, is_plugin=False,
         option={'icon': {'name': 'caise-aws'}}),

    dict(name="交换机", type=AutoDiscoveryType.SNMP, is_inner=True, is_plugin=False,
         option={'icon': {'name': 'caise-jiaohuanji'}}),
    dict(name="路由器", type=AutoDiscoveryType.SNMP, is_inner=True, is_plugin=False,
         option={'icon': {'name': 'caise-luyouqi'}}),
    dict(name="防火墙", type=AutoDiscoveryType.SNMP, is_inner=True, is_plugin=False,
         option={'icon': {'name': 'caise-fanghuoqiang'}}),
    dict(name="打印机", type=AutoDiscoveryType.SNMP, is_inner=True, is_plugin=False,
         option={'icon': {'name': 'caise-dayinji'}}),
]

ClOUD_MAP = {
    "aliyun": {
        "categories": ["云服务器 ECS"],
        "map": {
            "云服务器 ECS": "templates/aliyun_ecs.json",
        }
    },

    "tencentcloud": {
        "categories": ["云服务器 CVM"],
        "map": {
            "云服务器 CVM": "templates/tencent_cvm.json",
        }
    },

    "huaweicloud": {
        "categories": ["云服务器 ECS"],
        "map": {
            "云服务器 ECS": "templates/huaweicloud_ecs.json",
        }
    },

    "aws": {
        "categories": ["云服务器 EC2"],
        "map": {
            "云服务器 EC2": "templates/aws_ec2.json",
        }
    },
}
