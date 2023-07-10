/* eslint-disable */
import Vue from 'vue'
import router from './router'
import store from './store'

import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { setDocumentTitle, domTitle } from '@/utils/domUtil'
import config from '@/config/setting'
import { ACCESS_TOKEN } from './store/global/mutation-types'

NProgress.configure({ showSpinner: false })

// 不用认证的页面
const whitePath = ['/user/login', '/user/logout', '/user/register', '/api/sso/login', '/api/sso/logout', '/user/forgetPassword']

// 此处不处理登录, 只处理 是否有用户信息的认证  前端permission的处理  axios处理401 ->  登录
//  登录页面处理处理 是否使用单点登录
router.beforeEach((to, from, next) => {
  NProgress.start() // start progress bar
  to.meta && (!!to.meta.title && setDocumentTitle(`${to.meta.title} - ${domTitle}`))

  const authed = store.state.authed


  if (whitePath.includes(to.path)) {
    next()
  } else if ((config.useSSO || (!config.useSSO && Vue.ls.get(ACCESS_TOKEN))) && store.getters.roles.length === 0) {
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
  } else if (to.path === '/user/login' && !config.useSSO && store.getters.roles.length !== 0) {
    next({ path: '/' })
  } else if (!config.useSSO && !Vue.ls.get(ACCESS_TOKEN) && to.path !== '/user/login') {
    next({ path: '/user/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

router.afterEach(() => {
  NProgress.done()
})
