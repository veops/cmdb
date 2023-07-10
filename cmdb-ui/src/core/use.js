import Vue from 'vue'
import VueStorage from 'vue-ls'
import config from '@/config/setting'

// base library
import Antd from 'ant-design-vue'
import Viser from 'viser-vue'
import VueCropper from 'vue-cropper'
/* eslint-disable */
// import 'ant-design-vue/dist/antd.less'
import '../style/index.less'
// import 'element-ui/lib/theme-chalk/select.css';
// import 'element-ui/lib/theme-chalk/time-picker.css';
// import 'element-ui/lib/theme-chalk/icon.css';
// import 'element-ui/lib/theme-chalk/date-picker.css';
// import 'element-ui/lib/theme-chalk/button.css';
// import 'element-ui/lib/theme-chalk/autocomplete.css';
// import 'element-ui/lib/theme-chalk/time-select.css';
import 'element-ui/lib/theme-chalk/index.css'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
// ext library
import VueClipboard from 'vue-clipboard2'
import PermissionHelper from '@/utils/helper/permission'
// import '@/components/use'
import './directives/action'

import { VueAxios } from '../utils/request'
import 'xe-utils'
import VXETable from 'vxe-table'
import VXETablePluginExportXLSX from 'vxe-table-plugin-export-xlsx'
import 'vxe-table/lib/style.css'
import infiniteScroll from 'vue-infinite-scroll'
import EventBus from './EventBus'
import CustomDrawer from '@/components/CustomDrawer'
import CustomTransfer from '@/components/CustomTransfer'
import CustomRadio from '@/components/CustomRadio'
import CardTitle from '@/components/CardTitle'
import ElementUI from 'element-ui'
import Treeselect from '@riophae/vue-treeselect'
import OpsTable from '@/components/OpsTable'

Vue.config.productionTip = false
Vue.prototype.$bus = EventBus
Vue.use(VXETable)
VXETable.use(VXETablePluginExportXLSX)

Vue.config.productionTip = false

Vue.prototype.$bus = EventBus

Vue.use(VueAxios)
Vue.use(infiniteScroll)
Vue.use(ElementUI);

VueClipboard.config.autoSetContainer = true

Vue.prototype.$httpError = function (err, describe) {
  const prefix = describe || 'Http请求'
  const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
  this.$message.error(`${prefix}:${msg}`)
}

window.$message = Vue.prototype.$message

Vue.use(Antd)
Vue.use(Viser)

Vue.use(VueStorage, config.storageOptions)
Vue.use(VueClipboard)
Vue.use(PermissionHelper)
Vue.use(VueCropper)
Vue.component('CustomDrawer', CustomDrawer)
Vue.component('CustomTransfer', CustomTransfer)
Vue.component('CustomRadio', CustomRadio)
Vue.component('CardTitle', CardTitle)
Vue.component('Treeselect', Treeselect)
Vue.component('OpsTable', OpsTable)

