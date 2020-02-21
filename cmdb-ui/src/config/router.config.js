// eslint-disable-next-line
import store from '@/store'

import { UserLayout, BasicLayout, RouteView } from '@/layouts'
import { getPreference } from '@/api/cmdb/preference'

const cmdbRouter = [
  // resource views
  {
    path: '/resource_views',
    component: RouteView,
    name: 'cmdb_resource_views',
    meta: { title: 'menu.resourceViews', icon: 'hdd', keepAlive: true },
    children: []
  },
  // relation views
  {
    path: '/relation_views',
    component: () => import('@/views/cmdb/relation_views'),
    name: 'cmdb_relation_views',
    meta: { title: 'menu.relationViews', icon: 'link', keepAlive: true },
    hideChildrenInMenu: true,
    children: [
      {
        path: '/relation_views/:viewId',
        name: 'cmdb_relation_views_item',
        component: () => import('@/views/cmdb/relation_views'),
        meta: { title: 'menu.relationViews', keepAlive: true },
        hidden: true
      }]
  },
  // tree views
  {
    path: '/tree_views',
    component: () => import('@/views/cmdb/tree_views'),
    name: 'cmdb_tree_views',
    meta: { title: 'menu.treeViews', icon: 'share-alt', keepAlive: true },
    hideChildrenInMenu: true,
    children: [
      {
        path: '/tree_views/:typeId',
        name: 'cmdb_tree_views_item',
        component: () => import('@/views/cmdb/tree_views'),
        meta: { title: 'menu.treeViews', keepAlive: true },
        hidden: true
      }]
  },
  // preference
  {
    path: '/preference',
    component: () => import('@/views/cmdb/preference'),
    name: 'cmdb_preference',
    meta: { title: 'menu.preference', icon: 'star', keepAlive: true }
  },
  // batch
  {
    path: '/batch',
    component: () => import('@/views/cmdb/batch'),
    name: 'cmdb_batch',
    meta: { 'title': 'menu.batch', icon: 'upload', keepAlive: true }
  },
  {
    path: '/config/ci_types',
    name: 'cmdb_ci_type',
    component: RouteView,
    redirect: '/ci_types',
    meta: { title: 'menu.ciType', icon: 'setting', permission: ['admin'] },
    children: [
      {
        path: '/config/ci_types',
        name: 'ci_type',
        hideChildrenInMenu: true,
        component: () => import('@/views/cmdb/modeling/ci_type/list'),
        meta: { title: 'menu.ciModelManager', keepAlive: true }
      },
      {
        path: '/config/ci_types/:CITypeName/detail/:CITypeId',
        name: 'ci_type_detail',
        hideChildrenInMenu: true,
        component: () => import('@/views/cmdb/modeling/ci_type/detail'),
        meta: { title: 'menu.ciModelManager', keepAlive: true, hidden: true },
        hidden: true
      },
      {
        path: '/config/attributes',
        name: 'attributes',
        hideChildrenInMenu: true,
        component: () => import('@/views/cmdb/modeling/attributes/index'),
        meta: { title: 'menu.ciPropertyRep', keepAlive: true }
      },
      {
        path: '/config/relation_type',
        name: 'relation_type',
        hideChildrenInMenu: true,
        component: () => import('@/views/cmdb/modeling/relation_type/index'),
        meta: { title: 'menu.ciRelationType', keepAlive: true }
      },
      {
        path: '/config/preference_relation',
        name: 'preference_relation',
        hideChildrenInMenu: true,
        component: () => import('@/views/cmdb/modeling/preference_relation/index'),
        meta: { title: 'menu.ciRelationViewDefine', keepAlive: true }
      }
    ]
  },
  {
    path: '/acl',
    name: 'cmdb_acl',
    component: RouteView,
    redirect: '/acl/users',
    meta: { title: 'menu.acl', icon: 'safety-certificate', permission: ['admin'] },
    children: [
      {
        path: '/acl/users',
        name: 'cmdb_acl_users',
        hideChildrenInMenu: true,
        component: () => import('@/views/acl/users'),
        meta: { title: 'menu.aclUsersManager', keepAlive: true }
      },
      {
        path: '/acl/roles',
        name: 'cmdb_acl_roles',
        hideChildrenInMenu: true,
        component: () => import('@/views/acl/roles'),
        meta: { title: 'menu.aclRolesManager', keepAlive: true }
      },
      {
        path: '/acl/resources',
        name: 'cmdb_acl_resources',
        hideChildrenInMenu: true,
        component: () => import('@/views/acl/resources'),
        meta: { title: 'menu.aclResourceManager', keepAlive: true }
      },
      {
        path: '/acl/resource_types',
        name: 'cmdb_acl_resource_types',
        hideChildrenInMenu: true,
        component: () => import('@/views/acl/resource_types'),
        meta: { title: 'menu.aclResourceType', keepAlive: true }
      }
    ]
  }
]

function copyArray (arr) {
  return arr.map((e) => {
    if (typeof e === 'object') {
      return Object.assign({}, e)
    } else {
      return e
    }
  })
}

export const generatorDynamicRouter = () => {
  return new Promise((resolve, reject) => {
    // sub menu of the resource view
    getPreference().then(res => {
      const routers = copyArray(asyncRouterMap)
      routers[0].children = copyArray(cmdbRouter)
      let resourceMenus = []
      res.forEach(item => {
        resourceMenus.push({
          path: `/instances/types/${item.id}`,
          component: () => import(`@/views/cmdb/ci/index`),
          name: `cmdb_${item.id}`,
          meta: { title: item.alias, icon: 'table', keepAlive: true, typeId: item.id },
          hideChildrenInMenu: true
        })
      });
      routers[0].children[0].children = resourceMenus

      resolve(routers)
    })
  })
}

const asyncRouterMap = [
  {
    path: '/',
    name: 'cmdb',
    component: BasicLayout,
    meta: { title: 'CMDB', keepAlive: true },
    redirect: () => {
      return store.getters.addRouters[0].children.find(item => !item.hidden)
    }
  },
  {
    path: '*', redirect: '/404', hidden: true
  }
]

/**
 * basic route
 * @type { *[] }
 */
export const constantRouterMap = [
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/login',
    hidden: true,
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Login')
      },
      {
        path: 'register',
        name: 'register',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Register')
      },
      {
        path: 'register-result',
        name: 'registerResult',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/RegisterResult')
      }
    ]
  },

  {
    path: '/404',
    component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404')
  }

]
