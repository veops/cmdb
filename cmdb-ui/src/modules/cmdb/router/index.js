import { RouteView, BasicLayout } from '@/layouts'
import { getRelationView } from '@/modules/cmdb/api/preference'

const genCmdbRoutes = async () => {
  const routes = {
    path: '/cmdb',
    name: 'cmdb',
    component: BasicLayout,
    meta: { title: 'CMDB', keepAlive: false },
    redirect: '/cmdb/instances/types',
    children: [
      // preference
      // views
      {
        path: '/cmdb/dashboard',
        name: 'cmdb_dashboard',
        meta: { title: 'dashboard', icon: 'ops-cmdb-dashboard', selectedIcon: 'ops-cmdb-dashboard', keepAlive: false },
        component: () => import('../views/dashboard/index_v2.vue')
      },
      {
        path: '/cmdb/topoviews',
        name: 'cmdb_topology_views',
        meta: { title: 'cmdb.menu.topologyView', appName: 'cmdb', icon: 'ops-topology_view', selectedIcon: 'ops-topology_view', keepAlive: false },
        component: () => import('../views/topology_view/index.vue')
      },
      {
        path: '/cmdb/disabled1',
        name: 'cmdb_disabled1',
        meta: { title: 'cmdb.menu.resources', disabled: true },
      },
      {
        path: '/cmdb/relationviews/:viewId?',
        name: 'cmdb_relation_views',
        component: () => import('../views/relation_views/index'),
        meta: {
          title: 'cmdb.menu.serviceTree',
          appName: 'cmdb',
          icon: 'veops-servicetree',
          keepAlive: false
        },
      },
      {
        path: '/cmdb/instances/types/:typeId?',
        name: 'cmdb_resource_views',
        component: () => import(`../views/ci/index`),
        meta: { title: 'cmdb.menu.ciTable', icon: 'ops-cmdb-resource', selectedIcon: 'ops-cmdb-resource', keepAlive: false }
      },
      {
        path: '/cmdb/tree_views',
        component: () => import('../views/tree_views'),
        name: 'cmdb_tree_views',
        meta: { title: 'cmdb.menu.ciTree', icon: 'ops-cmdb-tree', selectedIcon: 'ops-cmdb-tree', keepAlive: false },
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
        hidden: true,
        meta: { title: 'cmdb.menu.ciSearch', icon: 'ops-cmdb-search', selectedIcon: 'ops-cmdb-search', keepAlive: false },
        component: () => import('../views/resource_search_2/index.vue')
      },
      {
        path: '/cmdb/adc',
        name: 'cmdb_auto_discovery_ci',
        meta: { title: 'cmdb.menu.adCIs', icon: 'ops-cmdb-adc', selectedIcon: 'ops-cmdb-adc', keepAlive: false, permission: ['admin', 'cmdb_admin'] },
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
        path: '/cmdb/disabled4',
        name: 'cmdb_disabled4',
        meta: { title: 'cmdb.menu.scene', appName: 'cmdb', disabled: true, permission: ['admin', 'cmdb_admin'] },
      },
      {
        path: '/cmdb/ipam',
        component: () => import('../views/ipam'),
        name: 'cmdb_ipam',
        meta: { title: 'IPAM', appName: 'cmdb', icon: 'veops-ipam', selectedIcon: 'veops-ipam', keepAlive: false, permission: ['admin', 'cmdb_admin'] }
      },
      {
        path: '/cmdb/dcim',
        component: () => import('../views/dcim'),
        name: 'cmdb_dcim',
        meta: { title: 'cmdb.menu.dcim', appName: 'cmdb', icon: 'veops-data_center', selectedIcon: 'veops-data_center', keepAlive: false, permission: ['cmdb_admin', 'admin'] }
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
        meta: { title: 'cmdb.menu.preference', icon: 'ops-cmdb-preference', selectedIcon: 'ops-cmdb-preference', keepAlive: false }
      },
      {
        path: '/cmdb/batch',
        component: () => import('../views/batch'),
        name: 'cmdb_batch',
        meta: { 'title': 'cmdb.menu.batchUpload', icon: 'ops-cmdb-batch', selectedIcon: 'ops-cmdb-batch', keepAlive: false }
      },
      {
        path: '/cmdb/ci_types',
        name: 'ci_type',
        component: () => import('../views/ci_types/index'),
        meta: { title: 'cmdb.menu.citypeManage', icon: 'ops-cmdb-citype', selectedIcon: 'ops-cmdb-citype', keepAlive: false, permission: ['cmdb_admin', 'admin'] }
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
        meta: { title: 'cmdb.menu.backendManage', icon: 'veops-setting2', selectedIcon: 'veops-setting2', permission: ['cmdb_admin', 'OneOPS_Application_Admin', 'admin'], },
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
            path: '/cmdb/discovery',
            name: 'discovery',
            component: () => import('../views/discovery/index'),
            meta: { title: 'cmdb.menu.ad', keepAlive: false, icon: 'ops-cmdb-adr', selectedIcon: 'ops-cmdb-adr-selected' }
          },
          {
            path: '/cmdb/operationhistory',
            name: 'operation_history',
            hideChildrenInMenu: true,
            component: () => import('../views/operation_history/index'),
            meta: { title: 'cmdb.menu.operationHistory', keepAlive: false, icon: 'ops-cmdb-operation', selectedIcon: 'ops-cmdb-operation-selected' }
          },
          {
            path: '/cmdb/modelrelation',
            name: 'model_relation',
            hideChildrenInMenu: true,
            component: () => import('../views/model_relation/index'),
            meta: { title: 'cmdb.menu.citypeRelation', keepAlive: false, icon: 'ops-cmdb-modelrelation', selectedIcon: 'ops-cmdb-modelrelation-selected' }
          },
          {
            path: '/cmdb/relationtype',
            name: 'relation_type',
            hideChildrenInMenu: true,
            component: () => import('../views/relation_type/index'),
            meta: { title: 'cmdb.menu.relationType', keepAlive: false, icon: 'ops-cmdb-relationtype', selectedIcon: 'ops-cmdb-relationtype-selected' }
          }
        ]
      }
    ]
  }
  // get service tree dynamic display menu
  const relation = await getRelationView()

  if (relation?.name2id?.length === 0) {
    const relationViewRouteIndex = routes.children?.findIndex?.((route) => route.name === 'cmdb_relation_views')
    if (relationViewRouteIndex >= 0) {
      routes.children.splice(relationViewRouteIndex, 1)
    }
  }

  return routes
}

export default genCmdbRoutes
