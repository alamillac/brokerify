import React from 'react';
import Logger from 'plugins/logger';
import Grid from '@material-ui/core/Grid';
import CollapsedSection from 'components/CollapsedSection.jsx';
import CardBox from 'components/CardBox.jsx';
import IndexActions from 'actions/IndexActions';
import IndexStores from 'stores/IndexStores';
import StockActions from 'actions/StockActions';
import StockStores from 'stores/StockStores';
import StockHistoricalStores from 'stores/StockHistoricalStores';
import StockHistoricalActions from 'actions/StockHistoricalActions';
import {formatCurrency, formatPercentage, formatFloat} from 'plugins/format';
import {color_threshold_style} from 'plugins/styles';
import PortfolioSection from './PortfolioSection.jsx';
import IndexSection from './IndexSection.jsx';
import StockSection from './StockSection.jsx';
import ChartSection from './ChartSection.jsx';

const logger = Logger.createLogger('Home');

logger.info('Init view');

const styles = {
    margin: '30px',
};

export default class Home extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            indices: [],
            stocks: [],
            stocksHistorical: [],
        };
    }

    componentDidMount() {
        this.index = IndexStores.listen(this._index_listener.bind(this));
        this.stock = StockStores.listen(this._stock_listener.bind(this));
        this.stockHistorical = StockHistoricalStores.listen(
            this._stock_historical_listener.bind(this),
        );
        IndexActions.fetch();
        StockActions.fetch();
        StockHistoricalActions.fetch('2017-06-20');
    }

    componentWillUnmount() {
        this.index();
        this.stock();
        this.stockHistorical();
    }

    _index_listener(response) {
        switch (response.type) {
            case 'FETCH_OK':
                this.setState({
                    indices: response.data,
                });
                break;
        }
    }

    _stock_listener(response) {
        switch (response.type) {
            case 'FETCH_OK':
                this.setState({
                    stocks: response.data,
                });
                break;
        }
    }

    _stock_historical_listener(response) {
        switch (response.type) {
            case 'FETCH_OK':
                this.setState({
                    stocksHistorical: response.data,
                });
                break;
        }
    }

    render() {
        const stocks = this.state.stocks
            .sort(
                (stock1, stock2) =>
                    stock2.stats.approx_valorization -
                    stock1.stats.approx_valorization,
            )
            .slice(0, 12);
        return (
            <div style={styles}>
                <PortfolioSection portfolios={this.props.user.portfolios} />
                <IndexSection indices={this.state.indices} />
                <StockSection stocks={stocks} />
                <ChartSection stocks={this.state.stocksHistorical} />
            </div>
        );
    }
}
