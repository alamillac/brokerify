import React from 'react';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Logger from 'plugins/logger';
import {formatCurrency, formatPercentage} from 'plugins/format';
import {color_threshold_style} from 'plugins/styles';

const logger = Logger.createLogger('PortfolioCard');

logger.info("Init view");

const styles = {
    'margin': '5px'
};

const PortfolioCard = (portfolio, i) => (
    <Grid item xs={3} key={i}>
        <Card key={i} style={styles}>
            <CardContent>
                <Typography color="textSecondary">
                    {portfolio.name}
                </Typography>
                <Typography variant="headline" component="h2">
                    {formatCurrency(portfolio.stocks_value, portfolio.currency)}
                </Typography>
                <Typography color="textSecondary">
                    <span style={color_threshold_style(portfolio.valorization, 1, 1)}>
                        Rentabilidad: {formatPercentage(portfolio.valorization - 1)}
                    </span>
                    <br />
                    Dividendos: {formatCurrency(portfolio.dividends, portfolio.currency)}
                    <br />
                    Valor inicial: {formatCurrency(portfolio.initial_value, portfolio.currency)}
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="small">Detalle</Button>
            </CardActions>
        </Card>
    </Grid>
);

export default PortfolioCard;
