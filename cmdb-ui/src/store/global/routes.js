import { generatorDynamicRouter, constantRouterMap } from '@/router/config'
import { searchPermResourceByRoleId } from '@/modules/acl/api/permission'
import store from '@/store'
import user from './user'
/**
 * 过滤账户是否拥有某一个权限，并将菜单从加载列表移除
 *
 * @param permission
 * @param route
 * @returns {boolean}
 */
async function hasPermission(permission, route) {
  return new Promise(async (resolve, reject) => {
    const { detailPermissions } = user.state
    if (route.meta && route.meta.permission) {
      const totalPer = [...route.meta.appName && detailPermissions[`${route.meta.appName}`] ? detailPermissions[`${route.meta.appName}`].map(item => item.name) : [], ...permission]
      let flag = false
      if (route.name === 'ci_type') {
        await searchPermResourceByRoleId(store.state.user.rid, {
          resource_type_id: 'page',
          app_id: 'cmdb',
        }).then(res => {
          const { resources } = res
          const _idx = resources.findIndex(item => item.name === '模型配置')
          flag = flag || (_idx > -1)
        })
      }
      resolve(route.meta.permission.some(item => totalPer.includes(item)) || flag)
    }
    resolve(true)
  })
}

async function filterAsyncRouter(routerMap, roles) {
  const filteredRoutes = []
  for (let i = 0; i < routerMap.length; i++) {
    const route = routerMap[i]
    const default_route = ['company_info', 'company_structure', 'company_group']
    if (default_route.includes(route.name)) {
      filteredRoutes.push(route)
    } else {
      await hasPermission(roles.permissions, route).then(async flag => {
        if (flag) {
          if (route.children && route.children.length) {
            route.children = await filterAsyncRouter(route.children, roles)
          }
          filteredRoutes.push(route)
        }
      })
    }
  }
  return filteredRoutes
}

const routes = {
  state: {
    routers: constantRouterMap,
    appRoutes: []
  },
  mutations: {
    SET_ROUTERS: (state, routers) => {
      state.appRoutes = routers
      state.routers = constantRouterMap.concat(routers)
    }
  },
  actions: {
    GenerateRoutes({ commit }, data) {
      return new Promise(resolve => {
        const { roles } = data
        generatorDynamicRouter().then(async routers => {
          const accessedRouters = await filterAsyncRouter(routers, roles)
          commit('SET_ROUTERS', accessedRouters)
          resolve(accessedRouters)
        })
      })
    }
  }
}
export default routes
