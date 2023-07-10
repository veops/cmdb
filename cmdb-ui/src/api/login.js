import api from './index'
import { axios } from '@/utils/request'
import config from '@/config/setting'
/**
 * login func
 * parameter: {
 *     username: '',
 *     password: '',
 *     remember_me: true,
 *     captcha: '12345'
 * }
 * @param parameter
 * @returns {*}
 */
export function login(data) {
  if (config.useSSO) {
    window.location.href = config.ssoLoginUrl
  } else {
    return axios({
      url: api.Login,
      method: 'POST',
      data: data
    })
  }
}

export function getSmsCaptcha(parameter) {
  return axios({
    url: api.SendSms,
    method: 'post',
    data: parameter
  })
}

export function getInfo() {
  return axios({
    url: api.UserInfo,
    method: 'get',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
}

export function logout() {
  if (config.useSSO) {
    window.location.replace(api.Logout)
  } else {
    return axios({
      url: api.Logout,
      method: 'post',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      }
    })
  }
}

/**
 * get user 2step code open?
 * @param parameter {*}
 */
export function get2step(parameter) {
  return axios({
    url: api.twoStepCode,
    method: 'post',
    data: parameter
  })
}

export function getAllUsers(params) {
  return axios({
    url: '/v1/acl/users',
    method: 'GET',
    params
  })
}
