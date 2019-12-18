import Vue from 'vue'
import router from './router'
import store from './store'

import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import notification from 'ant-design-vue/es/notification'
import { setDocumentTitle, domTitle } from '@/utils/domUtil'
import config from '@/config/defaultSettings'
import { ACCESS_TOKEN } from './store/mutation-types'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

router.beforeEach((to, from, next) => {
  NProgress.start() // start progress bar
  to.meta && (typeof to.meta.title !== 'undefined' && setDocumentTitle(`${to.meta.title} - ${domTitle}`))
  if ((config.useSSO || (!config.useSSO && Vue.ls.get(ACCESS_TOKEN))) && store.getters.roles.length === 0) {
    store
      .dispatch('GetInfo')
      .then(res => {
        const roles = res.result && res.result.role
        store.dispatch('GenerateRoutes', { roles }).then(() => {
          // 根据roles权限生成可访问的路由表
          // 动态添加可访问路由表
          router.addRoutes(store.getters.addRouters)

          const redirect = decodeURIComponent(from.query.redirect || to.path)
          if (to.path === redirect) {
            // hack方法 确保addRoutes已完成 ,set the replace: true so the navigation will not leave a history record
            next({ ...to, replace: true })
          } else {
            // 跳转到目的路由
            next({ path: redirect })
          }
        })
      })
      .catch((e) => {
        console.log(e)
        notification.error({
          message: '错误',
          description: '请求用户信息失败，请重试'
        })
        setTimeout(() => {
          store.dispatch('Logout')
        }, 3000)
      })
  } else if (to.path === '/user/login' && !config.useSSO && store.getters.roles.length !== 0) {
    next({ path: '/' })
    NProgress.done()
  } else if (!config.useSSO && !Vue.ls.get(ACCESS_TOKEN) && to.path !== '/user/login') {
    next({ path: '/user/login', query: { redirect: to.fullPath } })
    NProgress.done()
  } else {
    next()
  }
})

router.afterEach(() => {
  NProgress.done() // finish progress bar
})
