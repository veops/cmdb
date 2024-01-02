import { RouteView } from '@/layouts'

export const getAppAclRouter = (appName) => {
    return {
        path: `/${appName}/acl`,
        name: `${appName}_acl`,
        component: RouteView,
        redirect: `/${appName}/acl/users`,
        meta: { title: 'commonMenu.permission', icon: 'safety-certificate', permission: [`${appName}_admin`, 'admin'] }, // permission: 'admin'
        children: [
            {
                path: `/${appName}/acl/roles`,
                name: `${appName}_acl_roles`,
                hideChildrenInMenu: true,
                component: () => import('@/modules/acl/views/roles'),
                meta: { title: 'commonMenu.role', icon: 'team', keepAlive: true }
            },
            {
                path: `/${appName}/acl/resources`,
                name: `${appName}_acl_resources`,
                hideChildrenInMenu: true,
                component: () => import('@/modules/acl/views/resources'),
                meta: { title: 'commonMenu.resource', icon: 'credit-card', keepAlive: false }
            },
            {
                path: `/${appName}/acl/resource_types`,
                name: `${appName}_acl_resource_types`,
                hideChildrenInMenu: true,
                component: () => import('@/modules/acl/views/resource_types'),
                meta: { title: 'commonMenu.resourceType', icon: 'file-text', keepAlive: true }
            },
            {
                path: `/${appName}/acl/trigger`,
                name: `${appName}_acl_trigger`,
                hideChildrenInMenu: true,
                component: () => import('@/modules/acl/views/trigger'),
                meta: { title: 'commonMenu.trigger', icon: 'clock-circle', keepAlive: true }
            }
        ]
    }
}
