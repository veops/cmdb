const webpack = require('webpack')
const ThemeColorReplacer = require('webpack-theme-color-replacer')
const generate = require('@ant-design/colors/lib/generate').default
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin')

const webpackPlugins = [
  // Ignore all locale files of moment.js
  new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
  new MonacoWebpackPlugin({
    languages: ['python', 'shell', 'powershell', 'json', 'bat']
  })
]

function isMonacoAsset(assetName, asset) {
  if (!/\.js$/i.test(assetName)) {
    return false
  }

  if (/(^|[\\/])(editor|json|ts)\.worker\.js$/i.test(assetName)) {
    return true
  }

  try {
    const source = asset?.source?.()?.toString?.() || ''
    return source.includes('MonacoEnvironment') || source.includes('editorSimpleWorker')
  } catch (error) {
    return false
  }
}

function getAntdSerials(color) {
  // Lighten (similar to less's tint)
  const lightens = new Array(9).fill().map((t, i) => {
    return ThemeColorReplacer.varyColor.lighten(color, i / 10)
  })
  const colorPalettes = generate(color)
  return lightens.concat(colorPalettes)
}

function createThemeColorReplacer() {
  // generate theme color replacement styles
  const plugin = new ThemeColorReplacer({
    fileName: 'css/theme-colors-[contenthash:8].css',
    matchColors: getAntdSerials('#2f54eb'), // primary color series
    // change style selectors to solve style override issues
    changeSelector(selector) {
      switch (selector) {
        case '.ant-calendar-today .ant-calendar-date':
          return ':not(.ant-calendar-selected-date):not(.ant-calendar-selected-day)' + selector
        case '.ant-btn:focus,.ant-btn:hover':
          return '.ant-btn:focus:not(.ant-btn-primary),.ant-btn:hover:not(.ant-btn-primary)'
        case '.ant-steps-item-process .ant-steps-item-icon > .ant-steps-icon':
          return ':not(.ant-steps-item-process)' + selector
        case '.ant-btn.active,.ant-btn:active':
          return '.ant-btn.active:not(.ant-btn-primary),.ant-btn:active:not(.ant-btn-primary)'
        case '.ant-menu-horizontal>.ant-menu-item-active,.ant-menu-horizontal>.ant-menu-item-open,.ant-menu-horizontal>.ant-menu-item-selected,.ant-menu-horizontal>.ant-menu-item:hover,.ant-menu-horizontal>.ant-menu-submenu-active,.ant-menu-horizontal>.ant-menu-submenu-open,.ant-menu-horizontal>.ant-menu-submenu-selected,.ant-menu-horizontal>.ant-menu-submenu:hover':
        case '.ant-menu-horizontal > .ant-menu-item-active,.ant-menu-horizontal > .ant-menu-item-open,.ant-menu-horizontal > .ant-menu-item-selected,.ant-menu-horizontal > .ant-menu-item:hover,.ant-menu-horizontal > .ant-menu-submenu-active,.ant-menu-horizontal > .ant-menu-submenu-open,.ant-menu-horizontal > .ant-menu-submenu-selected,.ant-menu-horizontal > .ant-menu-submenu:hover':
          return '.ant-menu-horizontal > .ant-menu-item-active,.ant-menu-horizontal > .ant-menu-item-open,.ant-menu-horizontal > .ant-menu-item-selected,.ant-menu-horizontal:not(.ant-menu-dark) > .ant-menu-item:hover,.ant-menu-horizontal > .ant-menu-submenu-active,.ant-menu-horizontal > .ant-menu-submenu-open,.ant-menu-horizontal:not(.ant-menu-dark) > .ant-menu-submenu-selected,.ant-menu-horizontal:not(.ant-menu-dark) > .ant-menu-submenu:hover'
        case '.ant-menu-horizontal > .ant-menu-item-selected > a':
          return ':not(.ant-menu-horizontal)' + selector
        case '.ant-menu-horizontal > .ant-menu-item > a:hover':
          return ':not(.ant-menu-horizontal)' + selector
        default:
          return selector
      }
    },
  })

  const assetsExtractor = plugin.handler?.assetsExtractor
  const originalExtractAsset = assetsExtractor.extractAsset.bind(assetsExtractor)
  assetsExtractor.extractAsset = function(assetName, asset) {
    // Monaco generates a large runtime/worker bundle; this plugin scans all JavaScript files as potential CSS containers.
    // Skip Monaco-related artifacts to avoid stack overflow caused by excessive regular expression/recursive parsing during the build process.
    if (isMonacoAsset(assetName, asset)) {
      return []
    }

    return originalExtractAsset(assetName, asset)
  }

  return plugin
}

webpackPlugins.push(
  createThemeColorReplacer()
)

module.exports = {
  webpackPlugins
}
