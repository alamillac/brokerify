import React from 'react';
import Logger from 'plugins/logger';
import Grid from '@material-ui/core/Grid';
import CollapsedSection from 'components/CollapsedSection.jsx';
import PortfolioCard from 'components/PortfolioCard.jsx';
import IndexCard from 'components/IndexCard.jsx';
import StockCard from 'components/StockCard.jsx';
import IndexActions from 'actions/IndexActions';
import IndexStores from 'stores/IndexStores';
import StockActions from 'actions/StockActions';
import StockStores from 'stores/StockStores';

const logger = Logger.createLogger('Home');

logger.info("Init view");


const styles = {
    'margin': '30px'
};


export default class Home extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            indices: [],
            stocks: []
        };

    }

    componentDidMount() {
        this.index = IndexStores.listen(this._index_listener.bind(this));
        this.stock = StockStores.listen(this._stock_listener.bind(this));
        IndexActions.fetch();
        StockActions.fetch();
    }

    componentWillUnmount() {
        this.index();
        this.stock();
    }

    _index_listener(response) {
        switch(response.type) {
            case "FETCH_OK":
                this.setState({
                    indices: response.data
                });
                break;
        }
    }

    _stock_listener(response) {
        switch(response.type) {
            case "FETCH_OK":
                this.setState({
                    stocks: response.data
                });
                break;
        }
    }

    render() {
        return (
            <div style={styles}>
                <CollapsedSection title="Carteras" expanded={true}>
                    <Grid container spacing={24}>
                        { this.props.user.portfolios.map((portfolio, i) => PortfolioCard(portfolio, i)) }
                    </Grid>
                </CollapsedSection>
                <CollapsedSection title="Indices">
                    <Grid container spacing={24}>
                        { this.state.indices.map((index, i) => IndexCard(index, i)) }
                    </Grid>
                </CollapsedSection>
                <CollapsedSection title="Acciones (Top 12)">
                    <Grid container spacing={24}>
                        {
                            this.state.stocks.
                                sort((stock1, stock2) => stock2.approx_valorization - stock1.approx_valorization).
                                slice(0,12).
                                map((stock, i) => StockCard(stock, i))
                        }
                    </Grid>
                </CollapsedSection>
            </div>
        );
    }
}
