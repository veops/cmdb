import Vue from 'vue'
import router from './router'
import store from './store'

import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { setDocumentTitle, domTitle } from '@/utils/domUtil'
import { ACCESS_TOKEN } from './store/global/mutation-types'
import i18n from '@/lang'

NProgress.configure({ showSpinner: false })

// pages that do not require authentication
const whitePath = [
  '/user/login',
  '/user/logout',
  '/user/register',
  '/api/sso/login',
  '/api/sso/logout',
  '/user/forgetPassword'
]

// Only handle user info authentication here, not login logic.
// Frontend permission handling; axios handles 401 -> login.
// Login page handles whether to use SSO.
router.beforeEach(async (to, from, next) => {
  NProgress.start() // start progress bar
  to.meta && (!!to.meta.title && setDocumentTitle(`${i18n.t(to.meta.title)} - ${domTitle}`))

  const auth_type = localStorage.getItem('ops_auth_type')
  if (whitePath.includes(to.path)) {
    next()
  } else if ((auth_type || (!auth_type && Vue.ls.get(ACCESS_TOKEN))) && store.getters.roles.length === 0) {
    store.dispatch('GetAuthDataEnable')
    store.dispatch('GetInfo').then(res => {
      const roles = res.result && res.result.role
      store.dispatch('loadAllUsers')
      store.dispatch('loadAllEmployees')
      store.dispatch('loadAllDepartments')
      store.dispatch('GenerateRoutes', { roles }).then(() => {
        router.addRoutes(store.getters.appRoutes)
        const redirect = decodeURIComponent(from.query.redirect || to.path)
        if (to.path === redirect) {
          // Ensure addRoutes is complete, set replace: true so navigation will not leave a history record
          next({ ...to, replace: true })
        } else {
          // Redirect to the target route
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
