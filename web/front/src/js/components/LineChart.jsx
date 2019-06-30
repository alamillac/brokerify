import React, {useEffect} from 'react';
import Chart from 'chart.js';

function getRandomColor() {
    const getRandomValue = maxValue => Math.floor(Math.random() * maxValue),
        colorR = getRandomValue(255),
        colorG = getRandomValue(255),
        colorB = getRandomValue(255);
    return `rgb(${colorR}, ${colorG}, ${colorB}, 0.2)`;
}

const LineChart = ({stocks, attr = 'price'}) => {
    let refNode;

    useEffect(() => {
        if (stocks.length === 0) {
            return;
        }

        // Draw chart
        const reduceDataset = (result, stock) => {
            if (stock.historical.length === 0) {
                // Remove stocks without historical values
                return result;
            }
            const firstValue = stock.historical[0][attr];
            const color = getRandomColor();
            result.push({
                label: stock.name,
                data: stock.historical.map(h => ({
                    t: new Date(h.date),
                    y: h[attr] / firstValue,
                })),
                backgroundColor: color,
                borderColor: color,
            });
            return result;
        };
        const datasets = stocks.reduce(reduceDataset, []);
        new Chart(refNode, {
            type: 'line',
            data: {
                datasets: datasets,
            },
            options: {
                scales: {
                    xAxes: [
                        {
                            type: 'time',
                            time: {
                                unit: 'month',
                            },
                        },
                    ],
                },
            },
        });
    });

    return <canvas ref={node => (refNode = node)}></canvas>;
};

export default LineChart;
