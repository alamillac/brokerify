import React from 'react';
import Grid from '@material-ui/core/Grid';
import CollapsedSection from 'components/CollapsedSection.jsx';
import LineChart from 'components/LineChart.jsx';

const StockSection = ({stocks}) => {
    //const filteredStocks = stocks.slice(0, 10);
    const bankNames = [
        'CAIXABANK',
        'BANCO_SABADELL',
        'BANKIA',
        'BANKINTER',
        'BANK_OF_AMERICA',
        'Deutsche Bank',
        'BBVA',
        'SANTANDER',
        'JP_MORGAN',
        'Morgan Stanley',
    ];
    const filteredStocks = stocks.filter(stock =>
        bankNames.includes(stock.name),
    );
    return (
        <CollapsedSection title="Historical evolution">
            <Grid container spacing={24}>
                <LineChart stocks={filteredStocks} attr="price" />
            </Grid>
        </CollapsedSection>
    );
};

export default StockSection;
