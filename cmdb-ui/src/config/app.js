const appConfig = {
  buildModules: ['cmdb'], // 需要编译的模块
  useMessageNotice: false, // 是否启用消息通知
  useTodoNotice: false, //  是否启用ticket通知
  useClaimNotice: false, // 是否启动ticket claim 通知
  useDagReviewNotice: false, // 是否启用dag审核通知
  redirectTo: '/cmdb', // 首页的重定向路径
  buildAclToModules: true, // 是否在各个应用下 内联权限管理
  ssoLogoutURL: '/api/sso/logout',
  showDocs: false,
}

export default appConfig
