const getters = {
  device: state => state.app.device,
  theme: state => state.app.theme,
  color: state => state.app.color,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  nickname: state => state.user.name,
  username: state => state.user.username,
  uid: state => state.user.uid,
  rid: state => state.user.rid,
  welcome: state => state.user.welcome,
  roles: state => state.user.roles,
  userInfo: state => state.user.info,
  appRoutes: state => state.routes.appRoutes,
  multiTab: state => state.app.multiTab,
}

export default getters
