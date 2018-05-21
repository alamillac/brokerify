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
for index_name in AVAILABLE_INDEX:
    h_index = IndexHistoricalPrices.get(index_name, datetime.date.today())
    if h_index:
        logger.info("Price for index %s in date %s already exist", index_name, datetime.data.today())
        continue

    try:
        index_data = index_api(index_name)[0]
        prices.append(index_data)
    except:
        continue
logger.info("Saving index prices in db")
IndexHistoricalPrices.bulk_insert(prices)
logger.info("End get index data")


logger.info("Start get stock data")
data = get_data(Stock.all())
logger.info("Saving stock data in db")
StockHistoricalData.bulk_insert(data)
logger.info("End get stock data")
