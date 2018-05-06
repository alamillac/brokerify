class MarketNames:
    BME = "bme"
    NASDAQ = "nasdaq"
    NYSE = "nyse"


class IndexNames:
    IBEX35 = "ibex35"


class StockCodes:
# BME
    # IBEX35
    ABERTIS = "ABE.MC"
    ACCIONA = "ANA.MC"
    ACERINOX = "ACX.MC"
    ACS = "ACS.MC"
    AENA = "AENA.MC"
    AMADEUS_IT_GROUP = "AMS.MC"
    ARCELORMITTAL = "MTS.MC"
    BANCO_SABADELL = "SAB.MC"
    BANKIA = "BKIA.MC"
    BANKINTER = "BKT.MC"
    BBVA = "BBVA.MC"
    CAIXABANK = "CABK.MC"
    CELLNEX_TELECOM = "CLNX.MC"
    COLONIAL = "COL.MC"
    DIA = "DIA.MC"
    ENAGAS = "ENG.MC"
    ENDESA = "ELE.MC"
    FERROVIAL = "FER.MC"
    GAS_NATURAL = "GAS.MC"
    GRIFOLS = "GRF.MC"
    IAG = "IAG.MC"
    IBERDROLA = "IBE.MC"
    INDITEX = "ITX.MC"
    INDRA = "IDR.MC"
    MAPFRE = "MAP.MC"
    MEDIASET = "TL5.MC"
    MELIA_HOTELS = "MEL.MC"
    MERLIN_PROP = "MRL.MC"
    RED_ELECTRICA = "REE.MC"
    REPSOL = "REP.MC"
    SANTANDER = "SAN.MC"
    SIEMENS_GAMESA = "SGRE.MC"
    TECNICAS_REUNIDAS = "TRE.MC"
    TELEFONICA = "TEF.MC"
    VISCOFAN = "VIS.MC"

    # ALL
    BME = "BME.MC"

# NASDAQ
    FACEBOOK = "FB"
    GOOGLE = "GOOG"
    APPLE = "AAPL"
    AMAZON = "AMZN"
    NVIDIA = "NVDA"
    NETFLIX = "NFLX"
    INTEL = "INTC"
    MICROSOFT = "MSFT"
    PAYPAL = "PYPL"
    CISCO = "CSCO"
    TESLA = "TSLA"
    # ...

# NYSE
    TWITTER = "TWTR"
    ALIBABA = "BABA"
    JP_MORGAN = "JPM"
    NIKE = "NKE"
    IBM = "IBM"
    VISA = "V"
    MCDONALDS = "MCD"
    ORACLE = "ORCL"
    COCA_COLA = "KO"
    WALT_DISNEY = "DIS"
    MATERCARD = "MA"
    GENERAL_MOTORS = "GM"
    JOHNSON_JOHNSON = "JNJ"
    FORD = "F"
    DELTA_AIRLINES = "DAL"
    WALMART = "WMT"
    CITI_GROUP = "C"
    CHEVRON = "CVX"
    BANK_OF_AMERICA = "BAC"
    _3M = "MMM"
    # ...


class Index:
    def __init__(self, name, code=None):
        self.name = name
        self.code = code or name.lower()


class Stock:
    def __init__(self, name, code, market, index=None):
        self.name = name
        self.code = code
        self.market = market
        self.index = index


class Market:
    def __init__(self, name, stocks_data, code=None):
        self.name = name
        self.code = code or name.lower()

        # Create stocks
        stock_map = {}
        index_map = {}
        for stock_name, stock_code, index_name in stocks_data:
            index = None
            if index_name:
                try:
                    index = index_map[index_name]
                except KeyError:
                    index = Index(index_name)
                    index_map[index_name] = index
            stock_map[stock_code] = Stock(stock_name, stock_code, self, index)

        self.stocks = stock_map.values()
        self.index = index_map.values()
