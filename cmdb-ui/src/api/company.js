import { axios } from '@/utils/request'

export function getCompanyInfo() {
  return axios({
    url: '/common-setting/v1/company/info',
    method: 'get',
  })
}
export function postCompanyInfo(parameter) {
  return axios({
    url: '/common-setting/v1/company/info',
    method: 'post',
    data: parameter,
  })
}
export function putCompanyInfo(id, parameter) {
  return axios({
    url: `/common-setting/v1/company/info/${id}`,
    method: 'put',
    data: parameter,
  })
}

export function getDepartmentList(params) {
  // ?department_parent_id=-1 Query first-level departments, pass actual ids below
  return axios({
    url: '/common-setting/v1/department',
    method: 'get',
    params: params
  })
}
export function getAllDepartmentList(params) { // is_tree
  return axios({
    url: '/common-setting/v1/department/all',
    method: 'get',
    params: params
  })
}
export function postDepartment(departmentData) {
  // Create department parameters
  // department_name
  // department_director_id Department director ID, default 0
  // department_parent_id Parent department ID, default 0, must be existing department ID when not 0
  return axios({
    url: '/common-setting/v1/department',
    method: 'post',
    data: departmentData,
  })
}
export function putDepartmentById(department_id, departmentData) {
  // Modify department parameter departmentData
  // department_name
  // department_director_id Department director ID, default 0
  // department_parent_id Parent department ID, default 0, must be existing department ID when not 0
  return axios({
    url: `/common-setting/v1/department/${department_id}`,
    method: 'put',
    data: departmentData,
  })
}
export function deleteDepartmentById(department_id) {
  return axios({
    url: `/common-setting/v1/department/${department_id}`,
    method: 'delete',
  })
}
export function getParentDepartmentList(department_id) {
  return axios({
    url: '/common-setting/v1/department/allow_parent',
    method: 'get',
    params: department_id,
  })
}

// Get tree structure of all departments and employees
export function getAllDepAndEmployee(params) {
  return axios({
    url: '/common-setting/v1/department/all_with_employee',
    method: 'get',
    params
  })
}

// Update department sorting
export function updateDepartmentsSort(data) {
  return axios({
    url: '/common-setting/v1/department/update_sort',
    method: 'put',
    data
  })
}
