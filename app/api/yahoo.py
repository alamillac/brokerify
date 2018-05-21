#!/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import re
from bs4 import BeautifulSoup
from app.codes import MarketCodes

AVAILABLE_MARKETS = [MarketCodes.BME, MarketCodes.NYSE, MarketCodes.NASDAQ]

def api(stock):
    def parse(response, stock):
        def get_value(soup, name):
            line = soup.find("span", text=name).parent.parent.findAll("td")
            return line[1].text
        def get_value_js(response, name):
            return re.match(".+"+name+"\":{\"raw\":([^,]+),", response.replace('\n','')).group(1)
        def parse_percentage(value):
            return float(value.replace("%","").replace(",",".").replace("N/A", "0"))
        parser = BeautifulSoup(response, 'html.parser')
        growth_table = parser.find("th", text="Estimaciones de crecimiento").parent.parent.parent
        growth_current_year = get_value(growth_table, "Año actual")
        growth_next_year = get_value(growth_table, "Año siguiente")
        growth_next_five_year = get_value(growth_table, "Próximos 5 años (anualmente)")
        growth_previous_five_year = get_value(growth_table, "Últimos 5 años (anualmente)")

        # Target Price
        price = float(get_value_js(response, "currentPrice"))
        expected_price = float(get_value_js(response, "targetMeanPrice"))
        potential = (expected_price - price) * 100 / price
        return {
            "name": stock.name,
            "date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "value": price,
            "change": "",
            "change_percent": "",
            "volume": "",
            "mean_volume_60": "",
            "max_value": "",
            "min_value": "",
            "max_year": "",
            "min_year": "",
            "change_percent_year": "",
            "max_52": "",
            "min_52": "",
            "change_percent_52": "",
            "annual_return": "",
            "dividend_yield": "",
            "market_capitalization": "",
            "ratios": {
                "bpa": "",
                "bpa1A": "",
                "bpaProx": "",
                "ebidta": "",
                "ebidta1A": "",
                "ebidtaProx": "",
                "per": "",
                "perProx": "",
                "per1A": "",
            },
            "fundamental_analysis": {
                "expected_price": expected_price,
                "potential": potential,
                "growth_current_year": parse_percentage(growth_current_year),
                "growth_next_year": parse_percentage(growth_next_year),
                "growth_next_five_year": parse_percentage(growth_next_five_year)
            },
            "market": stock.market.name
        }

    code = stock.code
    url = "https://es.finance.yahoo.com/quote/{}/analysis".format(code)
    return parse(requests.get(url, params={"p": code}).text, stock)
