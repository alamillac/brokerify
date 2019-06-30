import React from 'react';
import Grid from '@material-ui/core/Grid';
import CollapsedSection from 'components/CollapsedSection.jsx';
import CardBox from 'components/CardBox.jsx';
import {color_threshold_style} from 'plugins/styles';
import {formatCurrency, formatPercentage, formatFloat} from 'plugins/format';

const IndicesSection = ({indices}) => (
    <CollapsedSection title="Indices">
        <Grid container spacing={24}>
            {indices.map((index, i) => (
                <CardBox
                    id={index.id}
                    key={i}
                    name={index.name}
                    detailPath="/index"
                    value={formatCurrency(index.value)}>
                    <span
                        style={color_threshold_style(
                            index.valorization_one_day,
                            1,
                            1,
                        )}>
                        Rentabilidad 1d:{' '}
                        {formatPercentage(index.valorization_one_day - 1)}
                    </span>
                    <br />
                    <span
                        style={color_threshold_style(
                            index.valorization_one_week,
                            1,
                            1,
                        )}>
                        Rentabilidad 1w:{' '}
                        {formatPercentage(index.valorization_one_week - 1)}
                    </span>
                    <br />
                    <span
                        style={color_threshold_style(
                            index.valorization_one_year,
                            1,
                            1,
                        )}>
                        Rentabilidad 1y:{' '}
                        {formatPercentage(index.valorization_one_year - 1)}
                    </span>
                </CardBox>
            ))}
        </Grid>
    </CollapsedSection>
);

export default IndicesSection;
