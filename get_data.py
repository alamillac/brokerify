#!/bin/env python
# -*- coding: utf-8 -*-

from api import BME, NASDAQ, NYSE, MarketNames, get_data

def float_to_str(value):
    return str(value).replace('.', ',')

data = get_data(BME.stocks + NASDAQ.stocks + NYSE.stocks)

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
        approx_valorization = (fixed_potential*0.6/2) + growth_next_five_year*0.2 + stock_data["dividend_yield"]
    else:
        approx_valorization = (fixed_potential*0.8/2) + stock_data["dividend_yield"]
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

print("################################")
print("CSV:")
for line in csv:
    print(";".join(line))
