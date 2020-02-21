/**
 * Project default configuration items
 * showLocale - Whether to display the Chinese and English switch buttons: boolean
 * defaultLang - Default display language: zh-CN | en-US
 * useSSO - Whether to use single sign-on: boolean
 * primaryColor - Default theme color, clean up localStorage if changing color does not take effect
 * navTheme - sidebar theme ['dark', 'light']
 * colorWeak - Color blindness mode
 * layout - Overall layout ['sidemenu', 'topmenu']
 * fixedHeader - Fix Header: boolean
 * fixSiderbar - Fix the left menu bar: boolean
 * autoHideHeader - Hide header as you scroll down: boolean
 * contentWidth - Content area layout: streaming | fixed
 *
 * storageOptions: {} - Vue-ls Plug-in configuration item (localStorage/sessionStorage)
 *
 */

export default {
  showLocale: true,
  defaultLang: 'zh-CN',
  useSSO: false,
  primaryColor: '#1890ff', // primary color of ant design
  navTheme: 'dark', // theme for nav menu
  layout: 'sidemenu', // nav menu position: sidemenu or topmenu
  contentWidth: 'Fixed', // layout of content: Fluid or Fixed, only works when layout is topmenu
  fixedHeader: true, // sticky header
  fixSiderbar: true, // sticky siderbar
  autoHideHeader: true, //  auto hide header
  colorWeak: false,
  multiTab: false,
  production: process.env.NODE_ENV === 'production' && process.env.VUE_APP_PREVIEW !== 'true',
  // vue-ls options
  storageOptions: {
    namespace: 'pro__', // key prefix
    name: 'ls', // name variable Vue.[ls] or this.[$ls],
    storage: 'local' // storage name session, local, memory
  }
}
