const webpack = require('webpack');

module.exports = {
  // parallel: false,
  filenameHashing: false,
  publicPath: './',
  devServer: {
    port: 8008//測試用伺服器運行端口，如有任何變動Case.vue亦需變更
  },
  configureWebpack: {
    plugins: [
      new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        'windows.jQuery': 'jquery',
      }),
    ],
  },
};