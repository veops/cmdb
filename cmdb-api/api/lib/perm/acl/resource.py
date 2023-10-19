# -*- coding:utf-8 -*-


from flask import abort
from flask import current_app

from api.extensions import db
from api.lib.perm.acl.audit import AuditCRUD
from api.lib.perm.acl.audit import AuditOperateType
from api.lib.perm.acl.audit import AuditScope
from api.lib.perm.acl.cache import ResourceCache
from api.lib.perm.acl.cache import ResourceGroupCache
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.const import ACL_QUEUE
from api.lib.perm.acl.resp_format import ErrFormat
from api.lib.perm.acl.trigger import TriggerCRUD
from api.models.acl import Permission
from api.models.acl import Resource
from api.models.acl import ResourceGroup
from api.models.acl import ResourceGroupItems
from api.models.acl import ResourceType
from api.models.acl import RolePermission
from api.tasks.acl import role_rebuild
from api.tasks.acl import update_resource_to_build_role


class ResourceTypeCRUD(object):
    cls = ResourceType

    @staticmethod
    def search(q, app_id, page=1, page_size=None):
        query = db.session.query(ResourceType).filter(
            ResourceType.deleted.is_(False)).filter(ResourceType.app_id == app_id)
        if q:
            query = query.filter(ResourceType.name.ilike('%{0}%'.format(q)))

        numfound = query.count()
        res = query.offset((page - 1) * page_size).limit(page_size)
        rt_ids = [i.id for i in res]
        perms = db.session.query(Permission).filter(Permission.deleted.is_(False)).filter(
            Permission.resource_type_id.in_(rt_ids))
        id2perms = dict()
        for perm in perms:
            id2perms.setdefault(perm.resource_type_id, []).append(perm.to_dict())

        return numfound, res, id2perms

    @classmethod
    def id2name(cls):
        return {i.id: i.name for i in ResourceType.get_by(to_dict=False)}

    @staticmethod
    def get_by_name(app_id, name):
        resource_type = ResourceType.get_by(first=True, app_id=app_id, name=name, to_dict=False)
        return resource_type

    @staticmethod
    def get_perms(rt_id):
        perms = Permission.get_by(resource_type_id=rt_id, to_dict=False)
        return [i.to_dict() for i in perms]

    @classmethod
    def add(cls, app_id, name, description, perms):
        ResourceType.get_by(name=name, app_id=app_id) and abort(400, ErrFormat.resource_type_exists.format(name))

        rt = ResourceType.create(name=name, description=description, app_id=app_id)

        _, current_perm_ids = cls.update_perms(rt.id, perms, app_id)

        AuditCRUD.add_resource_log(app_id, AuditOperateType.create,
                                   AuditScope.resource_type, rt.id, {}, rt.to_dict(),
                                   {'permission_ids': {'current': current_perm_ids, 'origin': []}, }
                                   )

        return rt

    @classmethod
    def update(cls, rt_id, **kwargs):
        kwargs.pop('app_id', None)

        rt = ResourceType.get_by_id(rt_id) or abort(404,
                                                    ErrFormat.resource_type_not_found.format("id={}".format(rt_id)))
        if 'name' in kwargs:
            other = ResourceType.get_by(name=kwargs['name'], app_id=rt.app_id, to_dict=False, first=True)
            if other and other.id != rt_id:
                return abort(400, ErrFormat.resource_type_exists.format(kwargs['name']))

        perms = kwargs.pop('perms', None)
        current_perm_ids = []
        existed_perm_ids = []

        if perms:
            existed_perm_ids, current_perm_ids = cls.update_perms(rt_id, perms, rt.app_id)

        origin = rt.to_dict()
        rt = rt.update(**kwargs)

        AuditCRUD.add_resource_log(rt.app_id, AuditOperateType.update,
                                   AuditScope.resource_type, rt.id, origin, rt.to_dict(),
                                   {'permission_ids': {'current': current_perm_ids, 'origin': existed_perm_ids}, }
                                   )

        return rt

    @classmethod
    def delete(cls, rt_id):
        rt = ResourceType.get_by_id(rt_id) or abort(
            404, ErrFormat.resource_type_not_found.format("id={}".format(rt_id)))

        Resource.get_by(resource_type_id=rt_id) and abort(400, ErrFormat.resource_type_cannot_delete)

        origin = rt.to_dict()

        existed_perm_ids, _ = cls.update_perms(rt_id, [], rt.app_id)

        rt.soft_delete()

        AuditCRUD.add_resource_log(rt.app_id, AuditOperateType.delete,
                                   AuditScope.resource_type, rt.id, origin, {},
                                   {'permission_ids': {'current': [], 'origin': existed_perm_ids}, }
                                   )

    @classmethod
    def update_perms(cls, rt_id, perms, app_id):
        existed = Permission.get_by(resource_type_id=rt_id, to_dict=False)
        existed_names = [i.name for i in existed]
        existed_ids = [i.id for i in existed]
        current_ids = []

        for i in existed:
            if i.name not in perms:
                i.soft_delete()
            else:
                current_ids.append(i.id)

        for i in perms:
            if i not in existed_names:
                p = Permission.create(resource_type_id=rt_id,
                                      name=i,
                                      app_id=app_id)
                current_ids.append(p.id)

        return existed_ids, current_ids


class ResourceGroupCRUD(object):
    cls = ResourceGroup

    @staticmethod
    def search(q, app_id, resource_type_id, page=1, page_size=None):
        query = db.session.query(ResourceGroup).filter(
            ResourceGroup.deleted.is_(False)).filter(ResourceGroup.app_id == app_id).filter(
            ResourceGroup.resource_type_id == resource_type_id)

        if q:
            query = query.filter(ResourceGroup.name.ilike("%{0}%".format(q)))

        numfound = query.count()

        return numfound, query.offset((page - 1) * page_size).limit(page_size)

    @staticmethod
    def get_items(rg_id):
        items = ResourceGroupItems.get_by(group_id=rg_id, to_dict=False)

        return [i.resource.to_dict() for i in items]

    @staticmethod
    def add(name, type_id, app_id, uid=None):
        ResourceGroup.get_by(name=name, resource_type_id=type_id, app_id=app_id) and abort(
            400, ErrFormat.resource_group_exists.format(name))
        rg = ResourceGroup.create(name=name, resource_type_id=type_id, app_id=app_id, uid=uid)

        AuditCRUD.add_resource_log(app_id, AuditOperateType.create,
                                   AuditScope.resource_group, rg.id, {}, rg.to_dict(), {})
        return rg

    @staticmethod
    def update(rg_id, items):
        rg = ResourceGroup.get_by_id(rg_id) or abort(
            404, ErrFormat.resource_group_not_found.format("id={}".format(rg_id)))

        existed = ResourceGroupItems.get_by(group_id=rg_id, to_dict=False)
        existed_ids = [i.resource_id for i in existed]

        for i in existed:
            if i.resource_id not in items:
                i.soft_delete()

        for _id in items:
            if _id not in existed_ids:
                ResourceGroupItems.create(group_id=rg_id, resource_id=_id)

        AuditCRUD.add_resource_log(rg.app_id, AuditOperateType.update,
                                   AuditScope.resource_group, rg.id, rg.to_dict(), rg.to_dict(),
                                   {'resource_ids': {'current': items, 'origin': existed_ids}, }
                                   )

    @staticmethod
    def delete(rg_id):
        rg = ResourceGroup.get_by_id(rg_id) or abort(
            404, ErrFormat.resource_group_not_found.format("id={}".format(rg_id)))

        origin = rg.to_dict()
        rg.soft_delete()

        items = ResourceGroupItems.get_by(group_id=rg_id, to_dict=False)
        existed_ids = []

        for item in items:
            existed_ids.append(item.resource_id)
            item.soft_delete()

        rebuild = set()
        for i in RolePermission.get_by(group_id=rg_id, to_dict=False):
            i.soft_delete()
            rebuild.add(i.rid)

        for _rid in rebuild:
            role_rebuild.apply_async(args=(_rid, rg.app_id), queue=ACL_QUEUE)

        ResourceGroupCache.clean(rg)

        AuditCRUD.add_resource_log(rg.app_id, AuditOperateType.delete,
                                   AuditScope.resource_group, rg.id, origin, {},
                                   {'resource_ids': {'current': [], 'origin': existed_ids}, }

                                   )


class ResourceCRUD(object):
    cls = Resource

    @staticmethod
    def _parse_resource_type_id(type_id, app_id):
        try:
            type_id = int(type_id)
        except ValueError:
            _type = ResourceType.get_by(name=type_id, app_id=app_id, first=True, to_dict=False)
            type_id = _type and _type.id

        return type_id

    @classmethod
    def search(cls, q, u, app_id, resource_type_id=None, page=1, page_size=None):
        query = Resource.query.filter(
            Resource.deleted.is_(False)).filter(Resource.app_id == app_id)

        if q:
            query = query.filter(Resource.name.ilike("%{0}%".format(q)))

        if u and UserCache.get(u):
            query = query.filter(Resource.uid == UserCache.get(u).uid)

        if resource_type_id:
            resource_type_id = cls._parse_resource_type_id(resource_type_id, app_id)

            query = query.filter(Resource.resource_type_id == resource_type_id)

        numfound = query.count()
        res = [i.to_dict() for i in query.offset((page - 1) * page_size).limit(page_size)]
        for i in res:
            user = UserCache.get(i['uid']) if i['uid'] else ''
            i['user'] = user and user.nickname

        return numfound, res

    @classmethod
    def add(cls, name, type_id, app_id, uid=None):
        type_id = cls._parse_resource_type_id(type_id, app_id)

        Resource.get_by(name=name, resource_type_id=type_id, app_id=app_id) and abort(
            400, ErrFormat.resource_exists.format(name))

        r = Resource.create(name=name, resource_type_id=type_id, app_id=app_id, uid=uid)

        from api.tasks.acl import apply_trigger
        triggers = TriggerCRUD.match_triggers(app_id, r.name, r.resource_type_id, uid)
        current_app.logger.info(triggers)
        for trigger in triggers:
            # auto trigger should be no uid
            apply_trigger.apply_async(args=(trigger.id,),
                                      kwargs=dict(resource_id=r.id, ), queue=ACL_QUEUE)

        AuditCRUD.add_resource_log(app_id, AuditOperateType.create,
                                   AuditScope.resource, r.id, {}, r.to_dict(), {})

        return r

    @staticmethod
    def update(_id, name):
        # todo trigger rebuild
        resource = Resource.get_by_id(_id) or abort(404, ErrFormat.resource_not_found.format("id={}".format(_id)))

        origin = resource.to_dict()

        other = Resource.get_by(name=name, resource_type_id=resource.resource_type_id, to_dict=False, first=True)
        if other and other.id != _id:
            return abort(400, ErrFormat.resource_exists.format(name))

        ResourceCache.clean(resource)

        resource = resource.update(name=name)

        update_resource_to_build_role.apply_async(args=(_id, resource.app_id), queue=ACL_QUEUE)

        AuditCRUD.add_resource_log(resource.app_id, AuditOperateType.update,
                                   AuditScope.resource, resource.id, origin, resource.to_dict(), {})

        return resource

    @staticmethod
    def delete(_id):
        resource = Resource.get_by_id(_id) or abort(404, ErrFormat.resource_not_found.format("id={}".format(_id)))

        origin = resource.to_dict()
        resource.soft_delete()

        ResourceCache.clean(resource)

        rebuilds = []
        for i in RolePermission.get_by(resource_id=_id, to_dict=False):
            i.soft_delete()
            rebuilds.append((i.rid, i.app_id))

        for rid, app_id in set(rebuilds):
            role_rebuild.apply_async(args=(rid, app_id), queue=ACL_QUEUE)

        AuditCRUD.add_resource_log(resource.app_id, AuditOperateType.delete,
                                   AuditScope.resource, resource.id, origin, {}, {})

    @classmethod
    def delete_by_name(cls, name, type_id, app_id):
        resource = Resource.get_by(name=name, resource_type_id=type_id, app_id=app_id) or abort(
            400, ErrFormat.resource_exists.format(name))

        return cls.delete(resource.id)

    @classmethod
    def update_by_name(cls, name, type_id, app_id, new_name):
        resource = Resource.get_by(name=name, resource_type_id=type_id, app_id=app_id) or abort(
            400, ErrFormat.resource_exists.format(name))

        return cls.update(resource.id, new_name)
