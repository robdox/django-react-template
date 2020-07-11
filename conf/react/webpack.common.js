const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  entry: [
    path.resolve(__dirname, 'src', 'index.jsx'),
  ],
  output: {
    path: path.resolve(__dirname, './build'),
    filename: 'bundle.js',
    publicPath: '/',
  },
  plugins: [
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin(
      {
        template: path.resolve(__dirname, 'public', 'index_template.ejs'),
        filename: './index.html'
      }
    ),
  ],
  context: path.join(__dirname),
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            plugins: [
              '@babel/plugin-syntax-dynamic-import',
              '@babel/plugin-transform-runtime',
              'lodash',
              [
                'babel-plugin-import',
                {
                  'libraryName': '@material-ui/core',
                  'camel2DashComponentName': false,
                },
                'core',
              ],
              [
                'babel-plugin-import',
                {
                  'libraryName': '@material-ui/icons',
                  'camel2DashComponentName': false,
                },
                'icons',
              ],
            ],
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
            ],
          },
        },
      },
      {
        test: /\.scss$/,
        use: [
          {
            loader: 'style-loader',
            options: {
              sourceMap: true,
            },
          },
          {
            loader: 'css-loader',
            options: {
              sourceMap: true,
            },
          },
          {
            loader: 'sass-loader',
            options: {
              data: '/static/css/style.css',
              sourceMap: true,
            },
          },
        ],
      },
      {
        test: /\.sass$/,
        use: [
          'css-loader',
          {
            loader: 'sass-loader',
            options: {
              indentedSyntax: true,
            },
          },
        ],
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: { importLoaders: 1 },
          },
          'postcss-loader',
        ],
      }, {
        test: /\.(gif|png|jpe?g|svg)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[path][name].[ext]',
            },
          },
        ],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css', '.scss', 'sass'],
    modules: [
      'node_modules',
      path.resolve(__dirname, './src'),
      path.resolve(__dirname, '.'),
    ],
  },
};
