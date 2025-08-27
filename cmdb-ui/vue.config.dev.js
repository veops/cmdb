const path = require('path')
const webpack = require('webpack')
const ThemeColorReplacer = require('webpack-theme-color-replacer')
const generate = require('@ant-design/colors/lib/generate').default

function resolve(dir) {
  return path.join(__dirname, dir)
}

// Development-specific Vue configuration
module.exports = {
  configureWebpack: {
    plugins: [
      // Ignore all locale files of moment.js
      new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
      // generate theme color replacement styles
      new ThemeColorReplacer({
        fileName: 'css/theme-colors-[contenthash:8].css',
        matchColors: getAntdSerials('#2f54eb'),
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
      }),
    ],
    // Development optimizations
    devtool: 'eval-cheap-module-source-map',
    optimization: {
      removeAvailableModules: false,
      removeEmptyChunks: false,
      splitChunks: false,
    },
  },

  chainWebpack: (config) => {
    config.resolve.alias.set('@$', resolve('src'))

    const svgRule = config.module.rule('svg')
    svgRule.uses.clear()
    svgRule
      .oneOf('inline')
      .resourceQuery(/inline/)
      .use('vue-svg-icon-loader')
      .loader('vue-svg-icon-loader')
      .end()
      .end()
      .oneOf('external')
      .use('file-loader')
      .loader('file-loader')
      .options({
        name: 'assets/[name].[hash:8].[ext]',
      })

    // Development-specific webpack optimizations
    if (process.env.NODE_ENV === 'development') {
      config.optimization.minimize(false)
      config.optimization.splitChunks({
        chunks: 'all',
        cacheGroups: {
          vendor: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          },
          common: {
            name: 'chunk-common',
            minChunks: 2,
            priority: 5,
            chunks: 'initial',
            reuseExistingChunk: true
          }
        }
      })
    }
  },

  css: {
    loaderOptions: {
      less: {
        modifyVars: {
          'primary-color': '#2f54eb',
        },
        javascriptEnabled: true,
      },
    },
    // Enable CSS hot reload
    extract: false,
  },

  pluginOptions: {
    'style-resources-loader': {
      preProcessor: 'less',
      patterns: [path.resolve(__dirname, './src/style/static.less')],
    },
  },

  devServer: {
    disableHostCheck: true,
    port: process.env.DEV_PORT || 8000,
    hot: true,
    liveReload: true,
    watchFiles: {
      paths: ['src/**/*'],
      options: {
        usePolling: true,
        interval: 1000,
      },
    },
    client: {
      overlay: {
        errors: true,
        warnings: false,
      },
      progress: true,
      reconnect: true,
    },
    compress: true,
    historyApiFallback: true,
    // Faster hot reload
    static: {
      directory: path.join(__dirname, 'public'),
      watch: true,
    },
    proxy: {
      '/api': {
        pathRewrite: {
          '^/api': '/api',
        },
        target: 'http://localhost:5000',
        changeOrigin: true,
        logLevel: 'debug',
      },
    },
  },

  // Development optimizations
  productionSourceMap: false,
  lintOnSave: false,
  transpileDependencies: [],
}

function getAntdSerials(color) {
  const lightens = new Array(9).fill().map((t, i) => {
    return ThemeColorReplacer.varyColor.lighten(color, i / 10)
  })
  const colorPalettes = generate(color)
  return lightens.concat(colorPalettes)
}
