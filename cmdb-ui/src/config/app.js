const appConfig = {
  buildModules: ['cmdb', 'acl'], // 需要编译的模块
  redirectTo: '/cmdb', // 首页的重定向路径
  buildAclToModules: true, // 是否在各个应用下 内联权限管理
  ssoLogoutURL: '/api/sso/logout',
  showDocs: false,
}

export default appConfig
