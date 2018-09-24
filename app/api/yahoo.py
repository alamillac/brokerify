#!/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import re
from bs4 import BeautifulSoup
from app.codes import MarketCodes

AVAILABLE_MARKETS = [MarketCodes.BME, MarketCodes.NYSE, MarketCodes.NASDAQ, MarketCodes.EURONEXT, MarketCodes.FRANKFURT]


def get_value(soup, name):
    line = soup.find("span", text=name).parent.parent.findAll("td")
    return line[1].text

def get_value_js(response, name):
    return re.match(".+"+name+"\":{\"raw\":([^,]+),", response.replace('\n', '')).group(1)

def parse_percentage(value):
    return float(value.replace("%", "").replace('.', '').replace(",", ".").replace("N/A", "0"))


def get_analysis(code):
    url = "https://es.finance.yahoo.com/quote/{}/analysis".format(code)
    response = requests.get(url, params={"p": code}).text

    parser = BeautifulSoup(response, 'html.parser')
    try:
        growth_table = parser.find("th", text="Estimaciones de crecimiento").parent.parent.parent
    except:
        return {}

    growth_current_year = get_value(growth_table, "Año actual")
    growth_next_year = get_value(growth_table, "Año siguiente")
    growth_next_five_year = get_value(growth_table, "Próximos 5 años (anualmente)")
    #growth_previous_five_year = get_value(growth_table, "Últimos 5 años (anualmente)")

    # Target Price
    price = float(get_value_js(response, "currentPrice"))
    expected_price = float(get_value_js(response, "targetMeanPrice"))
    potential = (expected_price - price) * 100 / price

    return {
        "value": price,
        "fundamental_analysis": {
            "expected_price": expected_price,
            "potential": potential,
            "growth_current_year": parse_percentage(growth_current_year),
            "growth_next_year": parse_percentage(growth_next_year),
            "growth_next_five_year": parse_percentage(growth_next_five_year)
        }
    }


def get_basic(code):
    url = "https://es.finance.yahoo.com/quote/{}".format(code)
    response = requests.get(url, params={"p": code}).text

    parser = BeautifulSoup(response, 'html.parser')
    try:
        summary_table = parser.find(id="quote-summary")
    except:
        return {}

    volume = get_value(summary_table, "Volumen")
    mean_volume = get_value(summary_table, "Media Volumen")
    interval = get_value(summary_table, "Intervalo de 52 semanas").split("-")
    interval_min = interval[0] if len(interval) == 2 else "0"
    interval_max = interval[1] if len(interval) == 2 else "0"
    bpa_ttm = get_value(summary_table, "BPA (TTM):")
    per_ttm = get_value(summary_table, "Ratio precio/beneficio (TMTM)")
    #capitalization = get_value(summary_table, "Capitalización de mercado")
    dividend = get_value(summary_table, "Previsión de rentabilidad y dividendo")
    dividend_percentage = re.search("\(([^)]+)\)", dividend).group(1)

    return {
        "volume": parse_percentage(volume),
        "mean_volume_60": parse_percentage(mean_volume),
        "max_52": parse_percentage(interval_max),
        "min_52": parse_percentage(interval_min),
        #"market_capitalization": parse_percentage(capitalization),
        "dividend_yield": parse_percentage(dividend_percentage),
        "ratios": {
            "bpa": parse_percentage(bpa_ttm),
            "per": parse_percentage(per_ttm)
        }
    }


def api(stock):
    result = {
        "name": stock.name,
        "code": stock.code,
        "date": datetime.date.today(),
        "value": "",
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
            "expected_price": "",
            "potential": "",
            "growth_current_year": "",
            "growth_next_year": "",
            "growth_next_five_year": ""
        },
        "market": stock.market.name
    }

    code = stock.code
    result.update(
        get_basic(code)
    )
    result.update(
        get_analysis(code)
    )
    return result
