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
  // ?department_parent_id=-1 查询第一级部门，下面的id根据实际的传
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
  // 创建部门参数
  // department_name
  // department_director_id 部门负责人ID, 默认 0
  // department_parent_id 上级部门ID， 默认0， 不为0时，必须是已存在的部门ID
  return axios({
    url: '/common-setting/v1/department',
    method: 'post',
    data: departmentData,
  })
}
export function putDepartmentById(department_id, departmentData) {
  // 修改部门参数departmentData
  // department_name
  // department_director_id 部门负责人ID, 默认 0
  // department_parent_id 上级部门ID， 默认0， 不为0时，必须是已存在的部门ID
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

// 获取全部部门和员工的树状结构
export function getAllDepAndEmployee(params) {
  return axios({
    url: '/common-setting/v1/department/all_with_employee',
    method: 'get',
    params
  })
}

// 更新部门排序
export function updateDepartmentsSort(data) {
  return axios({
    url: '/common-setting/v1/department/update_sort',
    method: 'put',
    data
  })
}
