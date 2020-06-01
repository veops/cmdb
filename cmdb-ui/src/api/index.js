import config from '@/config/defaultSettings'

const api = {
  Login: config.useSSO ? config.ssoLoginRedirectUrl : '/login',
  Logout: config.useSSO ? config.ssoLogoutRedirectUrl : '/logout',
  ForgePassword: '/auth/forge-password',
  Register: '/auth/register',
  twoStepCode: '/auth/2step-code',
  SendSms: '/account/sms',
  SendSmsErr: '/account/sms_err',
  // get my info
  UserInfo: '/v1/acl/users/info'
}
export default api
