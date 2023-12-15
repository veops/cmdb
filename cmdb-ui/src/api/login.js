import api from './index'
import { axios } from '@/utils/request'
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
export function login(data, auth_type) {
  if (auth_type) {
    localStorage.setItem('ops_auth_type', auth_type)
    window.location.href = `/api/${auth_type.toLowerCase()}/login`
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
  const auth_type = localStorage.getItem('ops_auth_type')
  localStorage.clear()
  return axios({
    url: auth_type ? `/${auth_type.toLowerCase()}/logout` : api.Logout,
    method: auth_type ? 'get' : 'post',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  })
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
