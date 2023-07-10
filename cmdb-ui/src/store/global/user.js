import Vue from 'vue'
import { login, getInfo, logout } from '@/api/login'
import { ACCESS_TOKEN } from '@/store/global/mutation-types'
import { welcome } from '@/utils/util'
import { getAllUsers } from '../../api/login'
import { searchPermResourceByRoleId } from '@/modules/acl/api/permission'
import { getEmployeeByUid, getEmployeeList } from '@/api/employee'
import { getAllDepartmentList } from '@/api/company'

const user = {
  state: {
    token: '',
    name: '',
    welcome: '',
    avatar: '',
    uid: 0,
    roles: [],
    info: {},
    authed: false,
    allUsers: [],
    allEmployees: [],
    allDepartments: [],
    detailPermissions: {
      'backend': [
        {
          'name': '公司信息',
          'permissions': ['read']
        },
        {
          'name': '公司架构',
          'permissions': ['read']
        },
        {
          'name': '用户分组',
          'permissions': ['read']
        }
      ]
    },
    username: '',
    mobile: '',
    department_id: undefined,
    employee_id: undefined,
    email: '',
    nickname: '',
    sex: '',
    position_name: '',
    direct_supervisor_id: null
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },

    SET_USER_INFO: (state, { name, welcome, avatar, roles, info, uid, username, mobile, department_id, employee_id, email, nickname, sex, position_name, direct_supervisor_id, annual_leave }) => {
      state.name = name
      state.welcome = welcome
      state.avatar = avatar
      state.roles = roles
      state.info = info
      state.uid = uid
      state.authed = true
      state.username = username
      state.mobile = mobile
      state.department_id = department_id
      state.employee_id = employee_id
      state.email = email
      state.nickname = nickname
      state.sex = sex
      state.position_name = position_name
      state.direct_supervisor_id = direct_supervisor_id
      state.annual_leave = annual_leave
    },

    LOAD_ALL_USERS: (state, users) => {
      state.allUsers = users
    },
    LOAD_ALL_EMPLOYEES: (state, allEmployees) => {
      state.allEmployees = allEmployees
    },
    LOAD_ALL_DEPARMTMENTS: (state, allDepartments) => {
      state.allDepartments = allDepartments
    },
    SET_DETAIL_PERMISSIONS: (state, data) => {
      state.detailPermissions = data.backend.length ? {
        ...state.detailPermissions,
        ...data
      } : state.detailPermissions
    },
  },

  actions: {
    // 登录
    Login({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        login(userInfo).then(response => {
          Vue.ls.set(ACCESS_TOKEN, response.token, 7 * 24 * 60 * 60 * 1000)
          commit('SET_TOKEN', response.token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo({ commit }) {
      return new Promise((resolve, reject) => {
        getInfo().then(response => {
          const result = response.result

          const role = result.role
          role.permissions = result.role.permissions
          role.permissions.map(per => {
            if (per.actionEntitySet != null && per.actionEntitySet.length > 0) {
              const action = per.actionEntitySet.map(action => { return action.action })
              per.actionList = action
            }
          })
          role.permissionList = role.permissions.map(permission => { return permission })
          searchPermResourceByRoleId(result.rid, {
            resource_type_id: '操作权限',
            app_id: 'backend',
          }).then(res => {
            commit('SET_DETAIL_PERMISSIONS', { backend: res.resources })
            resolve(response)
          })
          getEmployeeByUid(result.uid).then(res => {
            commit('SET_USER_INFO', {
              roles: result.role,
              info: result,
              name: result.name,
              welcome: welcome(),
              avatar: result.avatar,
              uid: result.uid,
              username: result.username,
              mobile: res.mobile,
              department_id: res.department_id,
              employee_id: res.employee_id,
              email: res.email,
              nickname: res.nickname,
              sex: res.sex,
              position_name: res.position_name,
              direct_supervisor_id: res.direct_supervisor_id,
              annual_leave: res.annual_leave
            })
          })
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    Logout({ commit, state }) {
      return new Promise((resolve) => {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        Vue.ls.remove(ACCESS_TOKEN)

        logout(state.token).then(() => {
          window.location.reload()
          resolve()
        }).catch(() => {
          resolve()
        })
      })
    },

    loadAllUsers({ commit, state }) {
      return new Promise((resolve, reject) => {
        getAllUsers({ page_size: 9999 }).then(res => {
          commit('LOAD_ALL_USERS', res.users)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    loadAllEmployees({ commit, state }) {
      return new Promise((resolve, reject) => {
        getEmployeeList({ page_size: 99999 }).then(res => {
          commit('LOAD_ALL_EMPLOYEES', res.data_list)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    loadAllDepartments({ commit, state }) {
      return new Promise((resolve, reject) => {
        getAllDepartmentList({ is_tree: 0 }).then(res => {
          commit('LOAD_ALL_DEPARMTMENTS', res)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    }
  }
}

export default user
