const appConfig = {
  buildModules: ['cmdb', 'acl'], // Modules to be compiled
  redirectTo: '/cmdb', // Redirect path for homepage
  buildAclToModules: true, // Whether to inline permission management in each application
  showDocs: false,
  useEncryption: true,
}

export default appConfig
