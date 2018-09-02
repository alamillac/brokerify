import React from 'react';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Logger from 'plugins/logger';
import {formatCurrency, formatPercentage, formatFloat} from 'plugins/format';
import {color_threshold_style} from 'plugins/styles';

const logger = Logger.createLogger('StockCard');

logger.info("Init view");

const styles = {
    'padding': '5px'
};

const StockCard = (stock, i) => (
    <Grid item xs={3} key={i}>
        <Card key={i} style={styles}>
            <CardContent>
                <Typography color="textSecondary">
                    {stock.stock.name}
                </Typography>
                <Typography variant="headline" component="h2">
                    {formatCurrency(stock.price, stock.stock.market.currency)}
                </Typography>
                <Typography color="textSecondary">
                    <span style={color_threshold_style(stock.approx_valorization, 10, 20)}>
                        Puntaje: {formatFloat(stock.approx_valorization)}
                    </span>
                    <br />
                    <span style={color_threshold_style(stock.per, 10, 25, true)}>
                        Per: {formatFloat(stock.per)}
                    </span>
                    <br />
                    <span style={color_threshold_style(stock.dividend_yield, 0, 4)}>
                        Dividendos: {formatFloat(stock.dividend_yield) + '%'}
                    </span>
                    <br />
                    <span style={color_threshold_style(stock.fixed_potential, 10, 30)}>
                        Potencial: {formatFloat(stock.fixed_potential) + '%'}
                    </span>
                    <br />
                    <span style={color_threshold_style(stock.growth_next_five_year, 5, 10)}>
                        Crecimiento Esperado (5y): {formatFloat(stock.growth_next_five_year) + '%'}
                    </span>
                    <br />
                    Precio esperado: {formatCurrency(stock.expected_price, stock.stock.market.currency)}
                    <br />
                    Fecha: {stock.date}
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="small">Detalle</Button>
            </CardActions>
        </Card>
    </Grid>
);

export default StockCard;
