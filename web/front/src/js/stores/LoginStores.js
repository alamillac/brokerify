'use strict';

import Reflux from 'reflux';
import Api from 'api';
import Logger from 'plugins/logger';
//import md5 from 'js-md5';
import LoginActions from "actions/LoginActions";


const logger = Logger.createLogger("LoginStores");

const LoginStores = Reflux.createStore({
    listenables: [LoginActions],
    init: function () {
        logger.info('Init Store.');
    },

    onLogin(username, password) {
        logger.info('On Login ');

        // Api request
        Api.post("/login", {username, password}).then((response) => {
            logger.info(response);
            logger.info('On Login Done:Success >> User Logged !! ');
            this.trigger({
                type: "LOGIN_OK",
                data: response
            });
        }).catch((err) => {
            logger.info('On Login Fail >> Not Loggin ');
            this.trigger({
                type: "LOGIN_ERROR",
                data: err
            });
        });
    },
    onLogout(){
        logger.info('On Logout ');
        Api.delete("/login", {}).then((response) => {
            logger.info(response);
            logger.info('On LOGOUT  Done:Success >> User Logged !! ');
            this.trigger({
                type: "LOGOUT_OK",
                data: null
            });
            window.location = "/login";
        }).catch((err) => {
            logger.info('On LOGOUT Fail >> Not Loggin ');
            this.trigger({
                type: "LOGOUT_ERROR",
                data: err
            });
        });
    }
});


export default LoginStores;
