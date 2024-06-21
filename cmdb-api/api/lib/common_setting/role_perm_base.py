class OperationPermission(object):

    def __init__(self, resource_perms):
        for _r in resource_perms:
            setattr(self, _r['page'], _r['page'])
            for _p in _r['perms']:
                setattr(self, _p, _p)


class BaseApp(object):
    resource_type_name = 'OperationPermission'
    all_resource_perms = []

    def __init__(self):
        self.admin_name = None
        self.roles = []
        self.app_name = 'acl'
        self.require_create_resource_type = self.resource_type_name
        self.extra_create_resource_type_list = []

        self.op = None

    @staticmethod
    def format_role(role_name, role_type, acl_rid, resource_perms, description=''):
        return dict(
            role_name=role_name,
            role_type=role_type,
            acl_rid=acl_rid,
            description=description,
            resource_perms=resource_perms,
        )


class CMDBApp(BaseApp):
    all_resource_perms = [
        {"page": "Big_Screen", "page_cn": "大屏", "perms": ["read"]},
        {"page": "Dashboard", "page_cn": "仪表盘", "perms": ["read"]},
        {"page": "Resource_Search", "page_cn": "资源搜索", "perms": ["read"]},
        {"page": "Auto_Discovery_Pool", "page_cn": "自动发现池", "perms": ["read"]},
        {"page": "My_Subscriptions", "page_cn": "我的订阅", "perms": ["read"]},
        {"page": "Bulk_Import", "page_cn": "批量导入", "perms": ["read"]},
        {"page": "Model_Configuration", "page_cn": "模型配置",
         "perms": ["read", "create_CIType", "create_CIType_group", "update_CIType_group",
                   "delete_CIType_group", "download_CIType"]},
        {"page": "Backend_Management", "page_cn": "后台管理", "perms": ["read"]},
        {"page": "Customized_Dashboard", "page_cn": "定制仪表盘", "perms": ["read"]},
        {"page": "Service_Tree_Definition", "page_cn": "服务树定义", "perms": ["read"]},
        {"page": "Model_Relationships", "page_cn": "模型关系", "perms": ["read"]},
        {"page": "Operation_Audit", "page_cn": "操作审计", "perms": ["read"]},
        {"page": "Relationship_Types", "page_cn": "关系类型", "perms": ["read"]},
        {"page": "Auto_Discovery", "page_cn": "自动发现", "perms": ["read", "create_plugin", "update_plugin", "delete_plugin"]},
        {"page": "TopologyView", "page_cn": "拓扑视图",
         "perms": ["read", "create_topology_group", "update_topology_group", "delete_topology_group",
                   "create_topology_view"],
         },
    ]

    def __init__(self):
        super().__init__()

        self.admin_name = 'cmdb_admin'
        self.app_name = 'cmdb'

        self.op = OperationPermission(self.all_resource_perms)
