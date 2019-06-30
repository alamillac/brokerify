import React from 'react';
import Grid from '@material-ui/core/Grid';
import CollapsedSection from 'components/CollapsedSection.jsx';
import CardBox from 'components/CardBox.jsx';
import {color_threshold_style} from 'plugins/styles';
import {formatCurrency, formatPercentage, formatFloat} from 'plugins/format';

const StockSection = ({stocks}) => (
    <CollapsedSection title="Acciones (Top 12)">
        <Grid container spacing={24}>
            {stocks.map((stock, i) => (
                <CardBox
                    id={stock.id}
                    key={i}
                    name={stock.name}
                    detailPath="/stock"
                    value={formatCurrency(
                        stock.stats.price,
                        stock.market.currency,
                    )}>
                    <span
                        style={color_threshold_style(
                            stock.stats.approx_valorization,
                            10,
                            20,
                        )}>
                        Puntaje: {formatFloat(stock.stats.approx_valorization)}
                    </span>
                    <br />
                    <span
                        style={color_threshold_style(
                            stock.stats.per,
                            10,
                            25,
                            true,
                        )}>
                        Per: {formatFloat(stock.stats.per)}
                    </span>
                    <br />
                    <span
                        style={color_threshold_style(
                            stock.stats.dividend_yield,
                            0,
                            4,
                        )}>
                        Dividendos:{' '}
                        {formatFloat(stock.stats.dividend_yield) + '%'}
                    </span>
                    <br />
                    <span
                        style={color_threshold_style(
                            stock.stats.fixed_potential,
                            10,
                            30,
                        )}>
                        Potencial:{' '}
                        {formatFloat(stock.stats.fixed_potential) + '%'}
                    </span>
                    <br />
                    <span
                        style={color_threshold_style(
                            stock.stats.growth_next_five_year,
                            5,
                            10,
                        )}>
                        Crecimiento Esperado (5y):{' '}
                        {formatFloat(stock.stats.growth_next_five_year) + '%'}
                    </span>
                    <br />
                    Precio esperado:{' '}
                    {formatCurrency(
                        stock.stats.expected_price,
                        stock.market.currency,
                    )}
                    <br />
                    Fecha: {stock.stats.date}
                </CardBox>
            ))}
        </Grid>
    </CollapsedSection>
);

export default StockSection;
