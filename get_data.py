#!/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
from app.models.core import Stock, StockHistoricalData, IndexHistoricalPrices, Index
from app.api import get_data, get_index_data


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Get_data")


logger.info("Start getting index data")
yesterday = (datetime.date.today() - datetime.timedelta(days=1))
index_to_search = [index for index in Index.all() if not IndexHistoricalPrices.get(index.code, yesterday)]
if index_to_search:
    prices = get_index_data(index_to_search, start_date=yesterday, end_date=yesterday)
    if prices:
        logger.info("Saving index prices in db")
        IndexHistoricalPrices.bulk_insert(prices)
logger.info("End get index data")


logger.info("Start get stock data")
stocks = Stock.all()
data = get_data(stocks)
logger.info("Saving stock data in db")
StockHistoricalData.bulk_insert(data)
logger.info("End get stock data")

stock_data = sorted([stock.get_data() for stock in stocks], key=lambda s: s.approx_valorization)
for data in stock_data:
    logger.info(data)
