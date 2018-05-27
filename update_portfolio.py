#!/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
import csv
from app.models.core import User, Portfolio, PortfolioStock, Stock
from app.codes import CurrencyCodes, StockCodes


def str_to_float(sfloat):
    return float(sfloat.replace(',','.'))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Update_portfolio")

map_stocks = {
    #"EUR3359109.TR": StockCodes.ANTENA_TRES,  # TODO adicionar a stocks
    "EUR410441.TR": StockCodes.BBVA,
    "EUR410457.TR": StockCodes.SANTANDER,
    "USD2559341.TR": StockCodes.FACEBOOK,
    "EUR420081.TR": StockCodes.INDITEX
}

user = User.get_or_create({
    "username": "alamilla",
    "name": "Andres",
    "lastname": "Lamilla"
})

portfolio = Portfolio.get_or_create({
    "user_id": user.id,
    "name": "largo_plazo",
    "currency": CurrencyCodes.EUR
})

logger.info("Start saving portfolio")
write_rows = []
with open("./portfolio_stock.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        write_rows.append(row)
        if int(row.get("Guardado")):
            continue

        date = datetime.datetime.strptime(row["Fecha"], "%Y-%m-%d").date()
        operation = PortfolioStock.Type.BUY if row["Operación"] == "Compra" else PortfolioStock.Type.SELL
        try:
            isin = row["Código/ISIN"]
            stock = Stock.get(map_stocks[isin])
        except KeyError:
            logger.warning("ISIN %s from %s not found", isin, row["Nombre"])
            continue

        data = {
            "portfolio_id": portfolio.id,
            "stock_id": stock.id,
            "type": operation,
            "date": date,
            "num_stocks": int(row["Cantidad"]),
            "price": str_to_float(row["Precio"]),
            "commission_price": str_to_float(row["Comisión"]),
            "exchange_rate": str_to_float(row["Tipo cambio"])
        }
        PortfolioStock.add(data)
        row["Guardado"] = 1

logger.info("Updating csv")
with open("./portfolio_stock.csv", 'w') as f:
    header = "Código/ISIN,Nombre,Divisa activo,Tipo de operación,Fecha,Precio,Tipo cambio,Cantidad,Comisión,Importe,Divisa,Operación,Guardado"
    writer = csv.DictWriter(f, fieldnames=header.split(','))
    writer.writeheader()
    for row in write_rows:
        writer.writerow(row)
logger.info("Done")
