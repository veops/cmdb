const appConfig = {
  buildModules: ['cmdb', 'acl', 'chart-demo'], // 需要编译的模块
  redirectTo: '/cmdb', // 首页的重定向路径
  buildAclToModules: false, // 是否在各个应用下 内联权限管理
  showDocs: false,
  useEncryption: false,
}

export default appConfig
