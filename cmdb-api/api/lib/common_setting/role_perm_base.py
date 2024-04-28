from api.lib.common_setting.const import RoleType


class OperationPermission(object):

    def __init__(self, resource_perms):
        for _r in resource_perms:
            setattr(self, f"{_r['page']}", _r['page'])
            for _p in _r['perms']:
                setattr(self, f"{_p}", _p)


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
        {"page": "Auto_Discovery", "page_cn": "自动发现", "perms": ["read"]}]

    def __init__(self):
        super().__init__()

        self.admin_name = 'cmdb_admin'
        self.app_name = 'cmdb'
        self.roles = self.parse_roles()

        self.op = OperationPermission(self.all_resource_perms)

    def parse_roles(self):
        return [self.cmdb_admin_role, self.cmdb_technician, self.cmdb_user]

    @property
    def cmdb_admin_role(self):
        return self.format_role(
            'CMDB管理员', RoleType.System, 0, self.all_resource_perms
        )

    @property
    def cmdb_technician(self):
        resource_perms_map = dict(
            Big_Screen=["read"],
            Dashboard=["read"],
            Resource_Search=["read"],
            Auto_Discovery_Pool=["read"],
            My_Subscriptions=["read"],
            Bulk_Import=["read"],
            Model_Configuration=["read", "create_CIType"],
            Backend_Management=[],
            Customized_Dashboard=[],
            Service_Tree_Definition=[],
            Model_Relationships=[],
            Operation_Audit=[],
            Relationship_Types=[],
            Auto_Discovery=[]
        )
        resource_perms = []
        for _page, _perms in resource_perms_map.items():
            resource_perms.append(
                dict(page=_page, perms=_perms)
            )

        return self.format_role(
            'CMDB技术员', RoleType.Technician, 0, resource_perms
        )

    @property
    def cmdb_user(self):
        resource_perms_map = dict(
            Big_Screen=["read"],
            Dashboard=["read"],
            Resource_Search=["read"],
            Auto_Discovery_Pool=["read"],
            My_Subscriptions=["read"],
            Bulk_Import=["read"],
            Model_Configuration=[],
            Backend_Management=[],
            Customized_Dashboard=[],
            Service_Tree_Definition=[],
            Model_Relationships=[],
            Operation_Audit=[],
            Relationship_Types=[],
            Auto_Discovery=[]
        )
        resource_perms = []
        for _page, _perms in resource_perms_map.items():
            resource_perms.append(
                dict(page=_page, perms=_perms)
            )

        return self.format_role(
            'CMDB用户', RoleType.User, 0, resource_perms
        )
