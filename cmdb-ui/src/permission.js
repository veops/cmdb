import Vue from 'vue'
import router from './router'
import store from './store'

import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import notification from 'ant-design-vue/es/notification'
import { setDocumentTitle, domTitle } from '@/utils/domUtil'
import config from '@/config/defaultSettings'
import { ACCESS_TOKEN } from './store/mutation-types'
import i18n from '@/locales'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

router.beforeEach((to, from, next) => {
  NProgress.start() // start progress bar
  var displayTitle

  if (to.meta && to.meta.title && to.meta.title.split('.')[0] === 'menu') {
    displayTitle = i18n.messages[i18n.locale].menu[to.meta.title.split('.')[1]]
  } else if (to.meta && to.meta.title) {
    displayTitle = to.meta.title
  }
  to.meta && (typeof to.meta.title !== 'undefined' && setDocumentTitle(`${displayTitle} - ${domTitle}`))
  if ((config.useSSO || (!config.useSSO && Vue.ls.get(ACCESS_TOKEN))) && store.getters.roles.length === 0) {
    store
      .dispatch('GetInfo')
      .then(res => {
        const roles = res.result && res.result.role
        store.dispatch('GenerateRoutes', { roles }).then(() => {
          // Generate an accessible routing table based on the roles permissions
          // Dynamically add accessible routing tables
          router.addRoutes(store.getters.addRouters)
          const redirect = decodeURIComponent(from.query.redirect || to.path)
          if (to.path === redirect) {
            // set the replace: true so the navigation will not leave a history record
            next({ ...to, replace: true })
          } else {
            // Jump to destination route
            next({ path: redirect })
          }
        })
      })
      .catch((e) => {
        notification.error({
          message: e.message,
          description: 'Failed to request user information. Please try again!'
        })
        setTimeout(() => {
          console.log('should re-login')
          store.dispatch('Login')
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
