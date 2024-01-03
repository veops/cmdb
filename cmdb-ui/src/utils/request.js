 /* eslint-dsiable */
import Vue from 'vue'
import axios from 'axios'
import { VueAxios } from './axios'
import message from 'ant-design-vue/es/message'
import notification from 'ant-design-vue/es/notification'
import { ACCESS_TOKEN } from '@/store/global/mutation-types'
import router from '@/router'
import store from '@/store'

// 创建 axios 实例
const service = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL, // api base_url
  timeout: 6000, // 请求超时时间
  withCredentials: true,
  crossDomain: true,
})

const err = (error) => {
  console.log(error)
  const reg = /5\d{2}/g
  if (error.response && reg.test(error.response.status)) {
    const errorMsg = ((error.response || {}).data || {}).message || '服务端未知错误, 请联系管理员！'
    message.error(errorMsg)
  } else if (error.response.status === 412) {
    let seconds = 5
    notification.warning({
      key: 'notification',
      message: 'WARNING',
      description:
        '修改已提交，请等待审核（5s）',
      duration: 5,
    })
    let interval = setInterval(() => {
      seconds -= 1
      if (seconds === 0) {
        clearInterval(interval)
        interval = null
        return
      }
      notification.warning({
        key: 'notification',
        message: 'WARNING',
        description:
          `修改已提交，请等待审核（${seconds}s）`,
        duration: seconds
      })
    }, 1000)
  } else if (error.config.url === '/api/v0.1/ci_types/can_define_computed' || error.config.isShowMessage === false) {
  } else {
    const errorMsg = ((error.response || {}).data || {}).message || '出现错误，请稍后再试'
    message.error(`${errorMsg}`)
  }
  if (error.response) {
    console.log(error.config.url)
    if (error.response.status === 401 && router.path === '/user/login') {
      window.location.href = '/user/logout'
    }
  }
  return Promise.reject(error)
}

// request interceptor
service.interceptors.request.use(config => {
  const token = Vue.ls.get(ACCESS_TOKEN)
  if (token) {
    config.headers['Access-Token'] = token // 让每个请求携带自定义 token 请根据实际情况自行修改
  }
  config.headers['Accept-Language'] = store?.state?.locale ?? 'zh'
  return config
}, err)

// response interceptor
service.interceptors.response.use((response) => {
  return response.data
}, err)

const installer = {
  vm: {},
  install(Vue) {
    Vue.use(VueAxios, service)
  }
}

export {
  installer as VueAxios,
  service as axios
}
