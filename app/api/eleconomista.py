#!/bin/env python

import requests
import datetime
from bs4 import BeautifulSoup
from app.codes import IndexCodes

AVAILABLE_INDEX = [IndexCodes.IBEX35]


def str2float(value):
    return float(value.replace(".","").replace(",","."))


def api(index_name, start_date=datetime.date.today(), end_date=datetime.date.today()):
    """
    Get current values of index
    """
    def parse(response, index_name):
        parser = BeautifulSoup(response, 'html.parser')
        table = parser.find("section", {"class": "general-tables"})
        results = []
        for row in table.findAll("tr"):
            values = row.findAll("td")
            if len(values) < 7:
                break

            date_raw, close_raw, var_raw, _, high_raw, low_raw, _ = [v.text for v in values]
            close_val = str2float(close_raw)
            var = str2float(var_raw)
            open_val = close_val - var
            date = datetime.datetime.strptime(date_raw, "%d/%m/%y").date()
            results.append({
                "name": index_name,
                "date": date,
                "open": open_val,
                "high": str2float(high_raw),
                "low": str2float(low_raw),
                "close": close_val
            })
        return results

    if index_name not in AVAILABLE_INDEX:
        raise Exception("Index %s not found", index_name)
    if start_date > end_date:
        raise Exception("Invalid date range")

    url = "http://www.eleconomista.es/indice/IBEX-35/historico-fechas/{}/{}".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    #TODO pagination
    return parse(requests.get(url).text, index_name)
