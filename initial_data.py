#!/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
import csv
from app.models.core import StockHistoricalData, IndexHistoricalPrices, Stock
from app.api.wall_street_journal import api as index_api, AVAILABLE_INDEX


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Get_data")


def str_to_float(sfloat):
    return float(sfloat.replace(',','.'))


logger.info("Start saving stock data")
with open("./stock_data.csv") as f:
    fieldnames = ("date", "name", "price", "expected_price", "max_52", "per", "growth_next_year", "growth_next_five_year", "dividend_yield")
    reader = csv.DictReader(f, fieldnames)

    for row in reader:
        stock = Stock.get_by_name(row["name"].replace(' ','_').replace('.', ''))
        if not stock:
            logger.warning("No stock found with name %s", row["name"])
            continue

        hist_data = StockHistoricalData.get_or_create({
            "date": datetime.datetime.strptime(row["date"], "%d/%m/%Y").date(),
            "code": stock.code,
            "price": str_to_float(row["price"]),
            "expected_price": str_to_float(row["expected_price"]),
            "max_52": str_to_float(row["max_52"]),
            "per": str_to_float(row["per"]),
            "growth_next_year": str_to_float(row["growth_next_year"]),
            "growth_next_five_year": str_to_float(row["growth_next_five_year"]),
            "dividend_yield": str_to_float(row["dividend_yield"])
        })


logger.info("Saving index prices in db")
prices = []
for index_name in AVAILABLE_INDEX:
    try:
        index_data = index_api(index_name, start_date=datetime.date(2018,5,4), end_date=datetime.date(2018,5,21))
        prices += index_data
    except:
        continue
IndexHistoricalPrices.bulk_insert(prices)
logger.info("Done")
