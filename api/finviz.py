#!/bin/env python

import requests
import datetime
from bs4 import BeautifulSoup
from stocks import MarketNames

AVAILABLE_MARKETS = [MarketNames.NYSE, MarketNames.NASDAQ]

def api(stock):
    def parse(response, stock):
        def get_value(soup, name):
            box = soup.find('td', text=name)
            return box.nextSibling.text

        parser = BeautifulSoup(response, 'html.parser')

        expected_price = float(get_value(parser, "Target Price"))
        price = float(get_value(parser, "Price"))
        potential = (expected_price - price) * 100 / price
        dividend = float(get_value(parser, "Dividend %").replace('%','').replace('-','0'))
        range_52w = get_value(parser, "52W Range").split('-')
        min_52 = float(range_52w[0])
        max_52 = float(range_52w[-1])

        per = float(get_value(parser, "P/E").replace('-','0'))
        perProx = float(get_value(parser, "Forward P/E"))

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
            "max_52": max_52,
            "min_52": min_52,
            "change_percent_52": "",
            "annual_return": "",
            "dividend_yield": dividend,
            "market_capitalization": "",
            "ratios": {
                "bpa": "",
                "bpa1A": "",
                "bpaProx": "",
                "ebidta": "",
                "ebidta1A": "",
                "ebidtaProx": "",
                "per": per,
                "perProx": perProx,
                "per1A": "",
            },
            "fundamental_analysis": {
                "expected_price": expected_price,
                "potential": potential,
                "growth_current_year": 0,
                "growth_next_year": 0,
                "growth_next_five_year": 0
            },
            "market": stock.market.name
        }

    code = stock.code
    url = "https://finviz.com/quote.ashx"
    return parse(requests.get(url, params={"t": code}).text, stock)
