#!/bin/env python

import requests
import datetime
from app.codes import StockCodes, MarketCodes

#AVAILABLE_MARKETS = [MarketCodes.BME, MarketCodes.NYSE, MarketCodes.NASDAQ]
AVAILABLE_MARKETS = [MarketCodes.BME]

codes = {
# BME
    StockCodes.ABERTIS: "M.ABE",
    StockCodes.ACCIONA: "M.ANA",
    StockCodes.ACERINOX: "M.ACX",
    StockCodes.ACS: "M.ACS",
    StockCodes.AENA: "M.AENA",
    StockCodes.AMADEUS_IT_GROUP: "M.AMS",
    StockCodes.ARCELORMITTAL: "M.MTS",
    StockCodes.BANCO_SABADELL: "M.SAB",
    StockCodes.BANKIA: "M.BKIA",
    StockCodes.BANKINTER: "M.BKT",
    StockCodes.BBVA: "M.BBVA",
    StockCodes.CAIXABANK: "M.CABK",
    StockCodes.CELLNEX_TELECOM: "M.CLNX",
    StockCodes.COLONIAL: "M.COL",
    StockCodes.DIA: "M.DIA",
    StockCodes.ENAGAS: "M.ENG",
    StockCodes.ENDESA: "M.ELE",
    StockCodes.FERROVIAL: "M.FER",
    StockCodes.GAS_NATURAL: "M.GAS",
    StockCodes.GRIFOLS: "M.GRF",
    StockCodes.IAG: "M.IAG",
    StockCodes.IBERDROLA: "M.IBE",
    StockCodes.INDITEX: "M.ITX",
    StockCodes.INDRA: "NEIDR",
    StockCodes.MAPFRE: "M.MAP",
    StockCodes.MEDIASET: "M.TL5",
    StockCodes.MELIA_HOTELS: "M.MEL",
    StockCodes.MERLIN_PROP: "M.MRL",
    StockCodes.RED_ELECTRICA: "M.REE",
    StockCodes.REPSOL: "M.REP",
    StockCodes.SANTANDER: "M.SAN",
    StockCodes.SIEMENS_GAMESA: "M.SGRE",
    StockCodes.TECNICAS_REUNIDAS: "M.TRE",
    StockCodes.TELEFONICA: "M.TEF",
    StockCodes.VISCOFAN: "M.VIS",
    StockCodes.BME: "M.BME",
    StockCodes.ATRESMEDIA: "M.A3M",

# NASDAQ
    StockCodes.FACEBOOK: "NQFB",
    StockCodes.GOOGLE: "NQGOOG",
    StockCodes.APPLE: "NQAAPL",
    StockCodes.AMAZON: "NQAMZN",
    StockCodes.NVIDIA: "NQNVDA",
    StockCodes.NETFLIX: "NQNFLX",
    StockCodes.INTEL: "NQINTC",
    StockCodes.MICROSOFT: "NQMSFT",
    StockCodes.PAYPAL: "NYPYPL",
    StockCodes.CISCO: "NQCSCO",
    StockCodes.TESLA: "NQTSLA",

# NYSE
    StockCodes.TWITTER: "NYTWTR",
    StockCodes.ALIBABA: "NQBABA",
    StockCodes.JP_MORGAN: "NYJPM",
    StockCodes.NIKE: "NYNKE",
    StockCodes.IBM: "NYIBM",
    StockCodes.VISA: "NYV",
    StockCodes.MCDONALDS: "NYMCD",
    StockCodes.ORACLE: "NYORCL",
    StockCodes.COCA_COLA: "NYKO",
    StockCodes.WALT_DISNEY: "NYDIS",
    StockCodes.MATERCARD: "NYMA",
    StockCodes.GENERAL_MOTORS: "NYGM",
    StockCodes.JOHNSON_JOHNSON: "NYJNJ",
    StockCodes.FORD: "NYF",
    StockCodes.DELTA_AIRLINES: "NYDAL",
    StockCodes.WALMART: "NYWMT",
    StockCodes.CITI_GROUP: "NYC",
    StockCodes.CHEVRON: "NYCHV",
    StockCodes.BANK_OF_AMERICA: "NYBAC",
    StockCodes._3M: "NYMMM",
}


# Expansion endpoint
def api(stock):
    def to_float(value, default=0):
        "18.109,12 => 18109.12"
        try:
            return float(value.replace(".", "").replace(",", "."))
        except ValueError:
            return default

    def parse(response, stock):
        data = response["valor"]
        date = datetime.datetime.strptime(data["fecha"], "%d/%m/%Y").date()
        ratios = data["ratios"]
        fundamental_analysis = data["analisis_fundamental"]
        technical_analysis = data["analisis_tecnico"]
        return {
            "name": data["nombre"],
            "code": stock.code,
            "date": date,
            "value": to_float(data["cotizacion"]),
            "change": to_float(data["cambio"]),
            "change_percent": to_float(data["cambio_porcentual"]),
            "volume": to_float(data["volumen"]),
            "mean_volume_60": to_float(data["media_volumen_60sesiones"]),
            "max_value": to_float(data["maximo"]),
            "min_value": to_float(data["minimo"]),
            "max_year": to_float(data["maximo_anyo"]),
            "min_year": to_float(data["minimo_anyo"]),
            "change_percent_year": to_float(data["porciento_anyo"]),
            "max_52": to_float(data["maximo_52s"]),
            "min_52": to_float(data["minimo_52s"]),
            "change_percent_52": to_float(data["porciento_52s"]),
            "annual_return": to_float(data["rentabilidad_anual"]),
            "dividend_yield": to_float(data["rentabilidad_dividendo"]),
            "market_capitalization": to_float(data["capitalizacion_bursatil"]),
            "ratios": {
                "bpa": float(ratios.get("bpa") or 0),
                "bpa1A": float(ratios.get("bpa1A") or 0),
                "bpaProx": float(ratios.get("bpaProx") or 0),
                "ebidta": float(ratios.get("ebidta") or 0),
                "ebidta1A": float(ratios.get("ebidta1A") or 0),
                "ebidtaProx": float(ratios.get("ebidtaProx") or 0),
                "per": float(ratios.get("per") or 0),
                "perProx": float(ratios.get("perProx") or 0),
                "per1A": float(ratios.get("per1A") or 0)
            },
            "fundamental_analysis": {
                "expected_price": float(fundamental_analysis.get("precio_objetivo") or 0),
                "potential": to_float(fundamental_analysis.get("potencial") or '0'),
                "growth_current_year": 0,
                "growth_next_year": 0,
                "growth_next_five_year": 0
            },
            "market": stock.market.name
            #TODO completar campos
        }

    url = "http://www.expansion.com/bolsa/datos/historico_valor.html"
    try:
        code = codes[stock.code]
    except KeyError:
        print("Error: Stock %s not found in this api" % stock.name)
    return parse(requests.get(url, params={"cod": code}).json(), stock)
