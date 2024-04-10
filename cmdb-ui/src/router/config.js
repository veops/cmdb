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
        hidden: true,
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
          meta: { title: 'cs.menu.person', },
          component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/person/index')
        },
        {
          path: '/setting/companyinfo',
          name: 'company_info',
          meta: { title: 'cs.menu.companyInfo', appName: 'backend', icon: 'ops-setting-companyInfo', selectedIcon: 'ops-setting-companyInfo-selected', permission: ['公司信息', 'backend_admin'] },
          component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/companyInfo/index')
        },
        {
          path: '/setting/companystructure',
          name: 'company_structure',
          meta: { title: 'cs.menu.companyStructure', appName: 'backend', icon: 'ops-setting-companyStructure', selectedIcon: 'ops-setting-companyStructure-selected', permission: ['公司架构', 'backend_admin'] },
          component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/companyStructure/index')
        },
        {
          path: '/setting/notice',
          name: 'notice',
          component: RouteView,
          meta: { title: 'cs.menu.notice', appName: 'backend', icon: 'ops-setting-notice', selectedIcon: 'ops-setting-notice-selected', permission: ['通知设置', 'backend_admin'] },
          redirect: '/setting/notice/email',
          children: [{
            path: '/setting/notice/email',
            name: 'notice_email',
            meta: { title: 'cs.menu.email', icon: 'ops-setting-notice-email', selectedIcon: 'ops-setting-notice-email-selected' },
            component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/notice/email/index')
          }, {
            path: '/setting/notice/wx',
            name: 'notice_wx',
            meta: { title: 'cs.menu.wx', icon: 'ops-setting-notice-wx', selectedIcon: 'ops-setting-notice-wx-selected' },
            component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/notice/wx')
          }, {
            path: '/setting/notice/dingding',
            name: 'notice_dingding',
            meta: { title: 'cs.menu.dingding', icon: 'ops-setting-notice-dingding', selectedIcon: 'ops-setting-notice-dingding-selected' },
            component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/notice/dingding')
          }, {
            path: '/setting/notice/feishu',
            name: 'notice_feishu',
            meta: { title: 'cs.menu.feishu', icon: 'ops-setting-notice-feishu', selectedIcon: 'ops-setting-notice-feishu-selected' },
            component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/notice/feishu')
          }]
        },
        {
          path: '/setting/auth',
          name: 'company_auth',
          meta: { title: 'cs.menu.auth', appName: 'backend', icon: 'ops-setting-auth', selectedIcon: 'ops-setting-auth-selected', permission: ['acl_admin'] },
          component: () => import(/* webpackChunkName: "setting" */ '@/views/setting/auth/index')
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
    path: '/user/logout',
    name: 'logout',
    component: () => import(/* webpackChunkName: "user" */ '@/views/user/Logout'),
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
