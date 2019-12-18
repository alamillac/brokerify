#!/bin/env python

import requests
import datetime
from app.codes import IndexCodes

AVAILABLE_INDEX = [IndexCodes.SP500, IndexCodes.DOW_JONES, IndexCodes.NASDAQ100]

def api(index_name, start_date=datetime.date.today(), end_date=datetime.date.today()):
    """
    Get current values of index
    """
    def parse(response, index_name):
        response_lines = response.split('\n')
        if len(response_lines) < 2:
            return []

        results = []
        for row in response_lines[1:]:
            row_values = row.split(',')
            date = datetime.datetime.strptime(row_values[0], "%m/%d/%y").date()
            if date < start_date or date > end_date:
                continue
            open_val, high_val, low_val, close_val = [float(val) for val in row_values[1:]]
            results.append({
                "name": index_name,
                "date": date,
                "open": open_val,
                "high": high_val,
                "low": low_val,
                "close": close_val
            })
        return results

    if index_name not in AVAILABLE_INDEX:
        raise Exception("Index not found")
    if start_date > end_date:
        raise Exception("Invalid date range")

    url = "http://quotes.wsj.com/index/{index}/historical-prices/download".format(index=index_name)
    params = {
        "MOD_VIEW": "page",
        "num_rows": 100,
        "range_days": 1,
        "startDate": start_date.strftime("%m/%d/%Y"),
        "endDate": end_date.strftime("%m/%d/%Y")
    }
    return parse(requests.get(url, params=params).text, index_name)
