module.exports = {
  presets: [
    '@vue/app',
    [
      '@babel/preset-env',
      {
        'useBuiltIns': 'usage', // "usage" | "entry" | false, defaults to false.
        'corejs': '3.1.2',
        'targets': {
          'esmodules': true,
          'ie': '11'
        }
      }
    ]
  ]
  // if your use import on Demand, Use this code
  // ,
  // plugins: [
  //   [ 'import', {
  //     'libraryName': 'ant-design-vue',
  //     'libraryDirectory': 'es',
  //     'style': true // `style: true` 会加载 less 文件
  //   } ]
  // ]
}
