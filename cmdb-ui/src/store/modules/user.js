import Vue from 'vue'
import { login, getInfo, logout } from '@/api/login'
import { ACCESS_TOKEN } from '@/store/mutation-types'
import { welcome } from '@/utils/util'

const user = {
  state: {
    token: '',
    name: '',
    welcome: '',
    avatar: '',
    roles: [],
    info: {}
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_NAME: (state, { name, welcome }) => {
      state.name = name
      state.welcome = welcome
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
    SET_INFO: (state, info) => {
      state.info = info
    }
  },

  actions: {
    // login
    Login ({ commit }, userInfo) {
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

    // get user info
    GetInfo ({ commit }) {
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
          commit('SET_ROLES', result.role)
          commit('SET_INFO', result)
          commit('SET_NAME', { name: result.name, welcome: welcome() })
          commit('SET_AVATAR', result.avatar)

          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // logout
    Logout ({ commit, state }) {
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
    }

  }
}

export default user
