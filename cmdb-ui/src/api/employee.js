import { axios } from '@/utils/request'

export function getEmployeeList(params) {
  return axios({
    url: '/common-setting/v1/employee',
    method: 'get',
    params: params,
  })
}
// export function getEmployeeList(params, orderBy) {
//   return axios({
//     url: '/common-setting/v1/employee' + '/' + orderBy,
//     method: 'get',
//     params: params,
//   })
// }
export function postEmployee(data) {
  return axios({
    url: '/common-setting/v1/employee',
    method: 'post',
    data: data,
  })
}
export function getEmployeeCount(params) {
  return axios({
    url: '/common-setting/v1/employee/count',
    method: 'get',
    params: params,
  })
}
export function deleteEmployee(_id) {
  return axios({
    url: `/common-setting/v1/employee/${_id}`,
    method: 'delete',
  })
}
export function putEmployee(_id, data) {
  return axios({
    url: `/common-setting/v1/employee/${_id}`,
    method: 'put',
    data: data,
  })
}
export function batchEditEmployee(data) {
  return axios({
    url: '/common-setting/v1/employee/batch',
    method: 'post',
    data: data,
  })
}
export function importEmployee(data) {
  return axios({
    url: '/common-setting/v1/employee/import',
    method: 'post',
    data
  })
}

export function getEmployeeByUid(uid) {
  return axios({
    url: `/common-setting/v1/employee/by_uid/${uid}`,
    method: 'get',
  })
}

export function updateEmployeeByUid(uid, data) {
  return axios({
    url: `/common-setting/v1/employee/by_uid/${uid}`,
    method: 'put',
    data
  })
}

export function updatePasswordByUid(uid, data) {
  return axios({
    url: `/common-setting/v1/employee/by_uid/change_password/${uid}`,
    method: 'put',
    data
  })
}

export function bindWxByUid(uid) {
  return axios({
    url: `/common-setting/v1/employee/by_uid/bind_work_wechat/${uid}`,
    method: 'put',
  })
}

export function getAllPosition() {
  return axios({
    url: `/common-setting/v1/employee/position`,
    method: 'get',
  })
}

export function getEmployeeByEmployeeId(employee_id) {
  return axios({
    url: `/common-setting/v1/employee/${employee_id}`,
    method: 'get',
  })
}

// 下载员工列表
export function downloadAllEmployee(params) {
  return axios({
    url: `/common-setting/v1/employee/export_all`,
    method: 'get',
    params,
    responseType: 'blob'
  })
}

export function getEmployeeListByFilter(data) {
  return axios({
    url: '/common-setting/v1/employee/filter',
    method: 'post',
    data
  })
}
