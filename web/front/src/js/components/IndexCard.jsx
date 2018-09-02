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

const logger = Logger.createLogger('IndexCard');

logger.info("Init view");

const styles = {
    'margin': '5px'
};

const IndexCard = (index, i) => (
    <Grid item xs={3} key={i}>
        <Card key={i} style={styles}>
            <CardContent>
                <Typography color="textSecondary">
                    {index.name}
                </Typography>
                <Typography variant="headline" component="h2">
                    {formatCurrency(index.value)}
                </Typography>
                <Typography color="textSecondary">
                    <span style={color_threshold_style(index.valorization_one_day, 1, 1)}>
                        Rentabilidad 1d: {formatPercentage(index.valorization_one_day - 1)}
                    </span>
                    <br />
                    <span style={color_threshold_style(index.valorization_one_week, 1, 1)}>
                        Rentabilidad 1w: {formatPercentage(index.valorization_one_week - 1)}
                    </span>
                    <br />
                    <span style={color_threshold_style(index.valorization_one_year, 1, 1)}>
                        Rentabilidad 1y: {formatPercentage(index.valorization_one_year - 1)}
                    </span>
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="small">Detalle</Button>
            </CardActions>
        </Card>
    </Grid>
);

export default IndexCard;
