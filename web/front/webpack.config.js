const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const envBuild = process.env.NODE_ENV || 'develop';

const APP_SRC = path.resolve(__dirname, 'src');

// PLUGINS
let plugins = [
    new HtmlWebpackPlugin({
        title: 'Brokerify',
        filename: 'index.html',
        template: APP_SRC + '/index.ejs',
        inject: 'body'
    }),
    new webpack.DefinePlugin({
        __ENV_BUILD__: JSON.stringify(envBuild)
    }),
    new webpack.HotModuleReplacementPlugin()
];

module.exports = {
    entry: ['whatwg-fetch', APP_SRC + '/js/index.js'],
    output: {
        path: path.resolve('dist'),
        filename: 'bundle.js',
        publicPath: '/'
    },
    module: {
        rules: [{
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            use: ['babel-loader']
        }]
    },
    devServer: {
        historyApiFallback: true,
        hot: true
    },
    plugins: plugins,
    resolve: {
        modules: [path.resolve(APP_SRC, 'js'), "node_modules"],
        alias: {
            config: path.resolve(APP_SRC, 'config.json'),
        },
        extensions: ['*', '.js', '.jsx']
    }
};
