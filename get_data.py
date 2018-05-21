#!/bin/env python
# -*- coding: utf-8 -*-

import logging
from app.models.core import Stock
from app.api import get_data
from app.api.wall_street_journal import api as index_api, AVAILABLE_INDEX

def float_to_str(value):
    return str(value).replace('.', ',')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Get_data")

logger.info("Start get stock data")
data = get_data(Stock.all())
logger.info("End get stock data")

logger.info("Start get index data")
for index_name in AVAILABLE_INDEX:
    try:
        index_data = index_api(index_name)[0]
    except:
        continue
logger.info("End get index data")

logger.info("Start formatting data")
csv = []
header = ["Fecha", "Nombre", "Mercado", "Precio actual", "Precio objetivo", "Precio maximo 52s", "Potencial %", "Potencial ajustado %", "Per", "Crecimiento prox año", "Crecimiento 5 años", "Dividendos", "Valorizacion anual aprox"]
for stock_data in data:
    expected_price = stock_data["fundamental_analysis"]["expected_price"]
    if expected_price == 0:
        expected_price = stock_data["max_52"] * 0.85
    expected_price_fixed = min(
        expected_price,
        (expected_price + stock_data["max_52"])/2
    )
    fixed_potential = (expected_price_fixed - stock_data["value"]) * 100 / stock_data["value"]
    growth_next_five_year = stock_data["fundamental_analysis"]["growth_next_five_year"]
    if growth_next_five_year:
        approx_valorization = (fixed_potential*0.5) + growth_next_five_year*0.2 + stock_data["dividend_yield"]*0.3
    else:
        approx_valorization = (fixed_potential*0.7) + stock_data["dividend_yield"]*0.3
    line = [
        stock_data["date"],
        stock_data["name"],
        stock_data["market"],
        float_to_str(stock_data["value"]),
        float_to_str(stock_data["fundamental_analysis"]["expected_price"]),
        float_to_str(stock_data["max_52"]),
        float_to_str(stock_data["fundamental_analysis"]["potential"]),
        float_to_str(fixed_potential),
        float_to_str(stock_data["ratios"]["per"]),
        float_to_str(stock_data["fundamental_analysis"]["growth_next_year"]),
        float_to_str(stock_data["fundamental_analysis"]["growth_next_five_year"]),
        float_to_str(stock_data["dividend_yield"]),
        float_to_str(approx_valorization)
    ]
    csv.append(line)

csv = [header] + sorted(csv, reverse=True, key=lambda e: float(e[-1].replace(',', '.')))

logger.info("################################")
logger.info("CSV:")
for line in csv:
    logger.info(";".join(line))
