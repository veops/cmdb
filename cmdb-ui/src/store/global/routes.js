import { generatorDynamicRouter, constantRouterMap } from '@/router/config'
import user from './user'
/**
 * 过滤账户是否拥有某一个权限，并将菜单从加载列表移除
 *
 * @param permission
 * @param route
 * @returns {boolean}
 */
function hasPermission(permission, route) {
  const { detailPermissions } = user.state
  if (route.meta && route.meta.permission) {
    // let flag = false
    // for (let i = 0, len = permission.length; i < len; i++) {
    //   flag = (route.meta.permission || []).includes(permission[i])
    //   if (flag) {
    //     return true
    //   }
    // }
    // return false
    const totalPer = [...route.meta.appName && detailPermissions[`${route.meta.appName}`] ? detailPermissions[`${route.meta.appName}`].map(item => item.name) : [], ...permission]
    return route.meta.permission.some(item => totalPer.includes(item))
  }
  return true
}

function filterAsyncRouter(routerMap, roles) {
  return routerMap.filter(route => {
    const default_route = ['company_info', 'company_structure', 'company_group']
    if (default_route.includes(route.name)) {
      return true
    }
    if (hasPermission(roles.permissions, route)) {
      if (route.children && route.children.length) {
        route.children = filterAsyncRouter(route.children, roles)
      }
      return true
    }
    return false
  })
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
        generatorDynamicRouter().then(routers => {
          const accessedRouters = filterAsyncRouter(routers, roles)
          commit('SET_ROUTERS', accessedRouters)
          resolve(accessedRouters)
        })
      })
    }
  }
}
export default routes
