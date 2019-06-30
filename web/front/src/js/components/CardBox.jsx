import React from 'react';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import {Link} from 'react-router-dom';

const styles = {
    margin: '5px',
};

const CardBox = ({id, name, value, children, detailPath}) => {
    return (
        <Grid item xs={3}>
            <Card style={styles}>
                <CardContent>
                    <Typography color="textSecondary">{name}</Typography>
                    <Typography variant="headline" component="h2">
                        {value}
                    </Typography>
                    <Typography color="textSecondary">{children}</Typography>
                </CardContent>
                <CardActions>
                    <Button
                        component={Link}
                        to={`${detailPath}/${id}`}
                        size="small">
                        Detalle
                    </Button>
                </CardActions>
            </Card>
        </Grid>
    );
};

export default CardBox;
