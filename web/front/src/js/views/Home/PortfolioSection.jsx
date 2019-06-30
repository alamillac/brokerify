import React from 'react';
import Grid from '@material-ui/core/Grid';
import CollapsedSection from 'components/CollapsedSection.jsx';
import CardBox from 'components/CardBox.jsx';
import {color_threshold_style} from 'plugins/styles';
import {formatCurrency, formatPercentage, formatFloat} from 'plugins/format';

const PortfolioSection = ({portfolios}) => (
    <CollapsedSection title="Carteras" expanded={true}>
        <Grid container spacing={24}>
            {portfolios.map((portfolio, i) => (
                <CardBox
                    id={portfolio.id}
                    key={i}
                    name={portfolio.name}
                    value={formatCurrency(
                        portfolio.stocks_value,
                        portfolio.currency,
                    )}
                    detailPath="/portfolio">
                    <span
                        style={color_threshold_style(
                            portfolio.valorization,
                            1,
                            1,
                        )}>
                        Rentabilidad:{' '}
                        {formatPercentage(portfolio.valorization - 1)}
                    </span>
                    <br />
                    Dividendos:{' '}
                    {formatCurrency(portfolio.dividends, portfolio.currency)}
                    <br />
                    Valor inicial:{' '}
                    {formatCurrency(
                        portfolio.initial_value,
                        portfolio.currency,
                    )}
                </CardBox>
            ))}
        </Grid>
    </CollapsedSection>
);

export default PortfolioSection;
