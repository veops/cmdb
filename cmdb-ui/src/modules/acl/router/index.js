import { BasicLayout, RouteView } from '@/layouts/index'
import { searchApp } from '@/modules/acl/api/app'

const genAppRoute = ({ name }) => {
  return {
    path: `/acl/${name}`,
    component: RouteView,
    meta: { title: name, icon: 'solution', permission: [`${name}_admin`, 'acl_admin'] },
    children: [
      {
        path: `/acl/${name}/roles`,
        name: `${name}_roles_acl`,
        hideChildrenInMenu: true,
        component: () => import('../views/roles'),
        meta: { title: 'acl.roleManage', icon: 'team', keepAlive: true }
      },
      {
        path: `/acl/${name}/resources`,
        name: `${name}_resources_acl`,
        hideChildrenInMenu: true,
        component: () => import('../views/resources'),
        meta: { title: 'acl.resourceManage', icon: 'credit-card', keepAlive: false }
      },
      {
        path: `/acl/${name}/resource_types`,
        name: `${name}_resource_types_acl`,
        hideChildrenInMenu: true,
        component: () => import('../views/resource_types'),
        meta: { title: 'acl.resourceType', icon: 'file-text', keepAlive: true }
      },
      {
        path: `/acl/${name}/trigger`,
        name: `${name}_trigger_acl`,
        hideChildrenInMenu: true,
        component: () => import('../views/trigger'),
        meta: { title: 'acl.trigger', icon: 'clock-circle', keepAlive: true }
      },
      {
        path: `/acl/${name}/history`,
        name: `${name}_history_acl`,
        hideChildrenInMenu: true,
        component: () => import('../views/history'),
        meta: { title: 'acl.history', icon: 'search', keepAlive: false }
      }
    ]
  }
}

const genAclRoutes = async () => {
  const aclApps = await searchApp()
  const routes = {
    path: '/acl',
    name: 'acl',
    component: BasicLayout,
    meta: { title: 'ACL', keepAlive: true },
    redirect: '/acl/secret_key',
    children: [
      {
        path: `/acl/secret_key`,
        name: 'acl_secret_key',
        component: () => import('../views/secretKey'),
        meta: { title: 'acl.userSecret', icon: 'key' }
      },
      {
        path: `/acl/operate_history`,
        name: 'acl_operate_history',
        component: () => import('../views/operation_history/index.vue'),
        meta: { title: 'acl.history', icon: 'search', permission: ['acl_admin'] }
      },
      {
        path: `/acl/user`,
        name: 'acl_user',
        component: () => import('../views/users'),
        meta: { title: 'acl.userManage', icon: 'user', permission: ['acl_admin'] }
      },
      {
        path: `/acl/roles`,
        name: `acl_roles`,
        component: () => import('../views/roles'),
        meta: { title: 'acl.roleManage', icon: 'team', keepAlive: true, permission: ['acl_admin'] }
      },
      {
        path: `/acl/apps`,
        name: 'acl_apps',
        component: () => import('../views/apps'),
        meta: { title: 'acl.appManage', icon: 'appstore', permission: ['acl_admin'] }
      }
    ]
  }

  aclApps.apps.forEach(app => {
    if (app.name !== 'acl') {
      routes.children.push(genAppRoute(app))
    }
  })
  return routes
}

export default genAclRoutes
