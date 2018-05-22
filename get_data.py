#!/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
from app.models.core import Stock, StockHistoricalData, IndexHistoricalPrices
from app.api import get_data
from app.api.wall_street_journal import api as index_api, AVAILABLE_INDEX


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Get_data")


logger.info("Start getting index data")
prices = []
yesterday = (datetime.date.today() - datetime.timedelta(days=1))
for index_name in AVAILABLE_INDEX:
    h_index = IndexHistoricalPrices.get(index_name, yesterday)
    if h_index:
        logger.info("Price for index %s in date %s already exist", index_name, yesterday)
        continue

    try:
        index_data = index_api(index_name, start_date=yesterday, end_date=yesterday)[0]
        prices.append(index_data)
    except:
        continue
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
