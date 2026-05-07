const path = require('path')
const { webpackPlugins } = require('./config/plugin.config')

function resolve(dir) {
  return path.join(__dirname, dir)
}

// vue.config.js
module.exports = {
  // runtimeCompiler: true,
  configureWebpack: {
    plugins: webpackPlugins,
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

    config.module
      .rule('monaco-font')
      .test(/\.ttf$/)
      .use('file-loader')
      .loader('file-loader')
      .options({
        name: 'fonts/[name].[hash:8].[ext]'
      })
  },

  css: {
    loaderOptions: {
      less: {
        modifyVars: {
          // override less variables for custom ant design theme
          'primary-color': '#2f54eb',
        },
        javascriptEnabled: true,
      },
    },
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
    proxy: {
      '/api': {
        pathRewrite: {
          '^/api': '/api',
        },
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },

  // disable source map in production
  productionSourceMap: false,
  lintOnSave: undefined,
  // babel-loader no-ignore node_modules/*
  transpileDependencies: [],
}
