/* eslint-disable */
import '@babel/polyfill'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/'
import bootstrap from './core/bootstrap'
import './core/use'
import './guard' // guard permission control
import './utils/filter' // global filter
import Setting from './config/setting'
import { Icon } from 'ant-design-vue'

import iconFont from '../public/iconfont/iconfont'

// 存在直接crash的风险 还未到
const customIcon = Icon.createFromIconfontCN(iconFont)
Vue.component('ops-icon', customIcon)
var vue;

async function start() {
  const _vue = new Vue({
    router,
    store,
    created: bootstrap,
    render: h => h(App)
  }).$mount('#app')
  vue = _vue

  if (process.env.NODE_ENV === 'development') {
    window.$app = vue
    window.$router = router
    window.$store = store
    window.$env = process.env
  }
}

start()
window.$setting = Setting

export default vue
