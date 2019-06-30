'use strict';

import Reflux from 'reflux';
import Logger from 'plugins/logger';
import StockHistoricalActions from 'actions/StockHistoricalActions';
import Api from 'api';

const logger = Logger.createLogger('StockHistoricalStores');

const StockHistoricalStores = Reflux.createStore({
    listenables: [StockHistoricalActions],
    init: function() {
        logger.info('Init Store.');
    },

    onFetch(initDate) {
        let filter = '';
        if (initDate) {
            filter = `?date=${initDate}`;
        }
        Api.get(`/api/historical/stock${filter}`)
            .then(response => {
                this.trigger({
                    type: 'FETCH_OK',
                    data: response,
                });
            })
            .catch(err => {
                this.trigger({
                    type: 'FETCH_KO',
                    data: err,
                });
            });
    },
});

export default StockHistoricalStores;
