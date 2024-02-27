import { RouteView, BasicLayout } from '@/layouts'
import { getPreference, getRelationView } from '@/modules/cmdb/api/preference'

const genCmdbRoutes = async () => {
  const routes = {
    path: '/cmdb',
    name: 'cmdb',
    component: BasicLayout,
    meta: { title: 'CMDB', keepAlive: false },
    children: [
      // preference
      // views
      {
        path: '/cmdb/dashboard',
        name: 'cmdb_dashboard',
        meta: { title: 'dashboard', icon: 'ops-cmdb-dashboard', selectedIcon: 'ops-cmdb-dashboard-selected', keepAlive: false },
        component: () => import('../views/dashboard/index_v2.vue')
      },
      {
        path: '/cmdb/disabled1',
        name: 'cmdb_disabled1',
        meta: { title: 'cmdb.menu.views', disabled: true },
      },
      {
        path: '/cmdb/resourceviews',
        name: 'cmdb_resource_views',
        component: RouteView,
        meta: { title: 'cmdb.menu.ciTable', icon: 'ops-cmdb-resource', selectedIcon: 'ops-cmdb-resource-selected', keepAlive: true },
        hideChildrenInMenu: false,
        children: []
      },
      {
        path: '/cmdb/tree_views',
        component: () => import('../views/tree_views'),
        name: 'cmdb_tree_views',
        meta: { title: 'cmdb.menu.ciTree', icon: 'ops-cmdb-tree', selectedIcon: 'ops-cmdb-tree-selected', keepAlive: false },
        hideChildrenInMenu: true,
        children: [
          {
            path: '/cmdb/tree_views/:typeId',
            name: 'cmdb_tree_views_item',
            component: () => import('../views/tree_views'),
            meta: { title: 'cmdb.menu.ciTree', keepAlive: false },
            hidden: true
          }]
      },
      {
        path: '/cmdb/resourcesearch',
        name: 'cmdb_resource_search',
        meta: { title: 'cmdb.menu.ciSearch', icon: 'ops-cmdb-search', selectedIcon: 'ops-cmdb-search-selected', keepAlive: false },
        component: () => import('../views/resource_search/index.vue')
      },
      {
        path: '/cmdb/adc',
        name: 'cmdb_auto_discovery_ci',
        meta: { title: 'cmdb.menu.adCIs', icon: 'ops-cmdb-adc', selectedIcon: 'ops-cmdb-adc-selected', keepAlive: false },
        component: () => import('../views/discoveryCI/index.vue')
      },
      {
        path: `/cmdb/cidetail/:typeId/:ciId`,
        name: 'cmdb_ci_detail',
        hidden: true,
        meta: { title: 'cmdb.menu.cidetail', keepAlive: false },
        component: () => import('../views/ci/ciDetailPage.vue')
      },
      {
        path: '/cmdb/disabled2',
        name: 'cmdb_disabled2',
        meta: { title: 'cmdb.menu.config', disabled: true, },
      },
      {
        path: '/cmdb/preference',
        component: () => import('../views/preference/index'),
        name: 'cmdb_preference',
        meta: { title: 'cmdb.menu.preference', icon: 'ops-cmdb-preference', selectedIcon: 'ops-cmdb-preference-selected', keepAlive: false }
      },
      {
        path: '/cmdb/batch',
        component: () => import('../views/batch'),
        name: 'cmdb_batch',
        meta: { 'title': 'cmdb.menu.batchUpload', icon: 'ops-cmdb-batch', selectedIcon: 'ops-cmdb-batch-selected', keepAlive: false }
      },
      {
        path: '/cmdb/ci_types',
        name: 'ci_type',
        component: () => import('../views/ci_types/index'),
        meta: { title: 'cmdb.menu.citypeManage', icon: 'ops-cmdb-citype', selectedIcon: 'ops-cmdb-citype-selected', keepAlive: false, permission: ['cmdb_admin', 'admin'] }
      },
      {
        path: '/cmdb/disabled3',
        name: 'cmdb_disabled3',
        meta: { title: 'cmdb.menu.backend', disabled: true, permission: ['cmdb_admin', 'OneOPS_Application_Admin', 'admin'], },
      },
      {
        path: '/cmdb/citypes',
        name: 'cmdb_ci_type',
        component: RouteView,
        redirect: '/cmdb/ci_type',
        meta: { title: 'cmdb.menu.backendManage', icon: 'setting', permission: ['cmdb_admin', 'OneOPS_Application_Admin', 'admin'], },
        children: [
          {
            path: '/cmdb/customdashboard',
            name: 'cmdb_custom_dashboard',
            component: () => import('../views/custom_dashboard/index'),
            meta: { title: 'cmdb.menu.customDashboard', keepAlive: false, icon: 'ops-cmdb-customdashboard', selectedIcon: 'ops-cmdb-customdashboard-selected' }
          },
          {
            path: '/cmdb/preferencerelation',
            name: 'preference_relation',
            component: () => import('../views/preference_relation/index'),
            meta: { title: 'cmdb.menu.serviceTreeDefine', keepAlive: false, icon: 'ops-cmdb-preferencerelation', selectedIcon: 'ops-cmdb-preferencerelation-selected' }
          },
          {
            path: '/cmdb/modelrelation',
            name: 'model_relation',
            hideChildrenInMenu: true,
            component: () => import('../views/model_relation/index'),
            meta: { title: 'cmdb.menu.citypeRelation', keepAlive: false, icon: 'ops-cmdb-modelrelation', selectedIcon: 'ops-cmdb-modelrelation-selected' }
          },
          {
            path: '/cmdb/operationhistory',
            name: 'operation_history',
            hideChildrenInMenu: true,
            component: () => import('../views/operation_history/index'),
            meta: { title: 'cmdb.menu.operationHistory', keepAlive: false, icon: 'ops-cmdb-operation', selectedIcon: 'ops-cmdb-operation-selected' }
          },
          {
            path: '/cmdb/relationtype',
            name: 'relation_type',
            hideChildrenInMenu: true,
            component: () => import('../views/relation_type/index'),
            meta: { title: 'cmdb.menu.relationType', keepAlive: false, icon: 'ops-cmdb-relationtype', selectedIcon: 'ops-cmdb-relationtype-selected' }
          },
          {
            path: '/cmdb/discovery',
            name: 'discovery',
            component: () => import('../views/discovery/index'),
            meta: { title: 'cmdb.menu.ad', keepAlive: false, icon: 'ops-cmdb-adr', selectedIcon: 'ops-cmdb-adr-selected' }
          },
        ]
      }
    ]
  }
  // Dynamically add subscription items and business relationships
  const [preference, relation] = await Promise.all([getPreference(), getRelationView()])

  preference.forEach(item => {
    routes.children[2].children.push({
      path: `/cmdb/instances/types/${item.id}`,
      component: () => import(`../views/ci/index`),
      name: `cmdb_${item.id}`,
      meta: { title: item.alias, keepAlive: false, typeId: item.id, name: item.name, customIcon: item.icon },
      // hideChildrenInMenu: true // Force display of MenuItem instead of SubMenu
    })
  })
  const lastTypeId = window.localStorage.getItem('ops_ci_typeid') || undefined
  if (lastTypeId && preference.some(item => item.id === Number(lastTypeId))) {
    routes.redirect = `/cmdb/instances/types/${lastTypeId}`
  } else if (routes.children[2].children.length > 0) {
    routes.redirect = routes.children[2].children.find(item => !item.hidden).path
  } else {
    routes.redirect = '/cmdb/dashboard'
  }
  const relationViews = relation.name2id.map(item => {
    return {
      path: `/cmdb/relationviews/${item[1]}`,
      name: `cmdb_relation_views_${item[1]}`,
      component: () => import('../views/relation_views/index'),
      meta: { title: item[0], icon: 'ops-cmdb-relation', selectedIcon: 'ops-cmdb-relation-selected', keepAlive: false, name: item[0] },
    }
  })
  routes.children.splice(2, 0, ...relationViews)
  return routes
}

export default genCmdbRoutes
