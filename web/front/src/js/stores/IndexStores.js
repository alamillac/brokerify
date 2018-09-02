'use strict';

import Reflux from 'reflux';
import Logger from 'plugins/logger';
import IndexActions from 'actions/IndexActions';
import Api from 'api';


const logger = Logger.createLogger("IndexStores");

const IndexStores = Reflux.createStore({
    listenables: [IndexActions],
    init: function () {
        logger.info('Init Store.');
    },

    onFetch() {
        Api.get("/api/index").then((response) => {
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

export default IndexStores;
