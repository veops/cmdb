/* eslint-disable */
import Vue from 'vue'
import router from './router'
import store from './store'

import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { setDocumentTitle, domTitle } from '@/utils/domUtil'
import { ACCESS_TOKEN } from './store/global/mutation-types'
import i18n from '@/lang'

NProgress.configure({ showSpinner: false })

// 不用认证的页面
const whitePath = ['/user/login', '/user/logout', '/user/register', '/api/sso/login', '/api/sso/logout', '/user/forgetPassword']

// 此处不处理登录, 只处理 是否有用户信息的认证  前端permission的处理  axios处理401 ->  登录
//  登录页面处理处理 是否使用单点登录
router.beforeEach(async (to, from, next) => {
  NProgress.start() // start progress bar
  to.meta && (!!to.meta.title && setDocumentTitle(`${i18n.t(to.meta.title)} - ${domTitle}`))

  const authed = store.state.authed
  const auth_type = localStorage.getItem('ops_auth_type')
  if (whitePath.includes(to.path)) {
    next()
  } else if ((auth_type || (!auth_type && Vue.ls.get(ACCESS_TOKEN))) && store.getters.roles.length === 0) {
    store.dispatch('GetAuthDataEnable')
    store.dispatch('GetInfo').then(res => {
      const roles = res.result && res.result.role
      store.dispatch("loadAllUsers")
      store.dispatch("loadAllEmployees")
      store.dispatch("loadAllDepartments")
      store.dispatch("getCompanyInfo")
      store.dispatch('GenerateRoutes', { roles }).then(() => {
        router.addRoutes(store.getters.appRoutes)
        const redirect = decodeURIComponent(from.query.redirect || to.path)
        if (to.path === redirect) {
          // hack方法 确保addRoutes已完成 ,set the replace: true so the navigation will not leave a history record
          next({ ...to, replace: true })
        } else {
          // 跳转到目的路由
          next({ path: redirect })
        }
      })
    }).catch((e) => {
      setTimeout(() => { store.dispatch('Logout') }, 3000)
    })
  } else if (to.path === '/user/login' && !auth_type && store.getters.roles.length !== 0) {
    next({ path: '/' })
  } else if (!auth_type && !Vue.ls.get(ACCESS_TOKEN) && to.path !== '/user/login') {
    await store.dispatch('GetAuthDataEnable')
    const { enable_list = [] } = store?.state?.user?.auth_enable ?? {}
    const _enable_list = enable_list.filter(en => en.auth_type !== 'LDAP')
    if (_enable_list.length === 1) {
      next({ path: '/user/logout', query: { redirect: to.fullPath } })
    } else {
      next({ path: '/user/login', query: { redirect: to.fullPath } })
    }
  } else {
    next()
  }
})

router.afterEach(() => {
  NProgress.done()
})
