/* eslint-disable */
import { UserLayout, BasicLayout, RouteView } from '@/layouts'
import appConfig from '@/config/app'
import { getAppAclRouter } from './utils'
import store from '../store'

export const generatorDynamicRouter = async () => {
  const packages = []
  const { apps = undefined } = store.getters.userInfo
  for (let appName of appConfig.buildModules) {
    if (!apps || !apps.length || apps.includes(appName)) {
      const module = await import(`@/modules/${appName}/index.js`)
      const r = await module.default.route()

      if (r.length) {
        if (module.default.name !== 'acl' && appConfig.buildAclToModules) {
          r[0].children.push(getAppAclRouter(module.default.name))
        }
        packages.push(...r)
      } else {
        if (module.default.name !== 'acl' && appConfig.buildAclToModules) {
          r.children.push(getAppAclRouter(module.default.name))
        }
        packages.push(r)
      }
    }
  }
  let routes = packages
  routes = routes.concat([
    { path: '*', redirect: '/404', hidden: true },
    {
      hidden: true,
      path: '/noticecenter',
      name: 'notice_center',
      component: BasicLayout,
      children: [{
        path: '/noticecenter',
        name: 'notice_center',
        meta: { title: '消息中心' },
        component: () => import(/* webpackChunkName: "setting" */ '@/views/noticeCenter/index')
      }]
    },
    {
      path: '/setting',
      component: BasicLayout,
      redirect: '/setting/companyinfo',
      meta: {},
      children: [
        {
          hidden: true,
          path: '/setting/person',
          name: 'setting_person',
          meta: { title: '个人中心', },
          component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/person/index')
        },
        {
          path: '/setting/companyinfo',
          name: 'company_info',
          meta: { title: '公司信息', appName: 'backend', icon: 'ops-setting-companyInfo', selectedIcon: 'ops-setting-companyInfo-selected', permission: ['acl_admin', 'backend_admin'] },
          component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/companyInfo/index')
        },
        {
          path: '/setting/companystructure',
          name: 'company_structure',
          meta: { title: '公司架构', appName: 'backend', icon: 'ops-setting-companyStructure', selectedIcon: 'ops-setting-companyStructure-selected', permission: ['acl_admin', 'backend_admin'] },
          component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/companyStructure/index')
        },
      ]
    },])
  return routes
}

/**
 * 基础路由
 */
export const constantRouterMap = [
  {
    path: '/',
    redirect: appConfig.redirectTo,
    // redirect: () => { return store.getters.appRoutes[0] },
  },
  {
    path: '/user/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "user" */ '@/views/user/Login'),
  },
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/login',
    hidden: true,
    children: [
      {
        path: 'register',
        name: 'register',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Register'),
      },
      {
        path: 'register-result',
        name: 'registerResult',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/RegisterResult'),
      },
    ],
  },
  {
    path: '/404',
    component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404'),
  },
  {
    path: '/403',
    component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/403'),
  },
  {
    path: '/500',
    component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/500'),
  },

]
