#!/bin/env python
# -*- coding: utf-8 -*-

import logging
from app.models.core import Stock, Index
import matplotlib.pyplot as plt
import pandas as pd


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Plot_data")


logger.info("Start index graph")
index_return = {}
for index in Index.all():
    index_return[index.name] = pd.Series({i['date']:i['return'] for i in index.get_return_from_date()})

pd.DataFrame(index_return).plot(grid=True)
plt.show()


logger.info("Start stock graph")
stock_oportunities = {}
for stock in Stock.all():
    s_return = stock.get_return_from_date()
    if s_return[-1]['return'] < 0.80:
        stock_oportunities[stock.name] = pd.Series({i['date']:i['return'] for i in s_return})

if stock_oportunities:
    pd.DataFrame(stock_oportunities).plot(grid=True)
    plt.show()
