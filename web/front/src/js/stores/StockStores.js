'use strict';

import Reflux from 'reflux';
import Logger from 'plugins/logger';
import StockActions from 'actions/StockActions';
import Api from 'api';


const logger = Logger.createLogger("StockStores");

const StockStores = Reflux.createStore({
    listenables: [StockActions],
    init: function () {
        logger.info('Init Store.');
    },

    onFetch() {
        Api.get("/api/stock").then((response) => {
            this.trigger({
                type: "FETCH_OK",
                data: response
            });
        }).catch((err) => {
            this.trigger({
                type: "FETCH_KO",
                data: err
            });
        });
    }
});

export default StockStores;
