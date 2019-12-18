// ie polyfill
import '@babel/polyfill'

import Vue from 'vue'
import EventBus from './EventBus'
import App from './App.vue'
import router from './router'
import store from './store/'
import { VueAxios } from './utils/request'

import bootstrap from './core/bootstrap'
import './core/use'
import './permission' // permission control
import './utils/filter' // global filter
Vue.config.productionTip = false

Vue.prototype.$bus = EventBus

// mount axios Vue.$http and this.$http
Vue.use(VueAxios)

new Vue({
  router,
  store,
  created: bootstrap,
  render: h => h(App)
}).$mount('#app')
