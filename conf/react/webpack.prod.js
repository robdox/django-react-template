var path = require('path')
var webpack = require('webpack')

const TerserPlugin = require('terser-webpack-plugin')

const merge = require('webpack-merge')
const common = require('./webpack.common.js')

process.env.NODE_ENV = 'production'

module.exports = merge(common, {
  mode: 'production',
  watch: false,
  devtool: 'source-map',
  watchOptions: {
    poll: false
  },
  optimization: {
    minimize: true,
    moduleIds: 'hashed',
    minimizer: [
      new TerserPlugin({
        cache: true,
        parallel: true,
        sourceMap: true,
      }),
    ],
    runtimeChunk: true,
    splitChunks: {
      chunks: 'all',
      maxAsyncRequests: 20,
      cacheGroups: {
        default: false,
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor_app',
          chunks: 'all',
          minChunks: 2
        }
      }
    }
  },
})
