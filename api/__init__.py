from stocks import Market, MarketNames, IndexNames, StockCodes
import expansion
import yahoo
import finviz


BME = Market(MarketNames.BME, [
    ("ABERTIS", StockCodes.ABERTIS, IndexNames.IBEX35),
    ("ACCIONA", StockCodes.ACCIONA, IndexNames.IBEX35),
    ("ACERINOX", StockCodes.ACERINOX, IndexNames.IBEX35),
    ("ACS", StockCodes.ACS, IndexNames.IBEX35),
    ("AENA", StockCodes.AENA, IndexNames.IBEX35),
    ("AMADEUS_IT_GROUP", StockCodes.AMADEUS_IT_GROUP, IndexNames.IBEX35),
    ("ARCELORMITTAL", StockCodes.ARCELORMITTAL, IndexNames.IBEX35),
    ("BANCO_SABADELL", StockCodes.BANCO_SABADELL, IndexNames.IBEX35),
    ("BANKIA", StockCodes.BANKIA, IndexNames.IBEX35),
    ("BANKINTER", StockCodes.BANKINTER, IndexNames.IBEX35),
    ("BBVA", StockCodes.BBVA, IndexNames.IBEX35),
    ("CAIXABANK", StockCodes.CAIXABANK, IndexNames.IBEX35),
    ("CELLNEX_TELECOM", StockCodes.CELLNEX_TELECOM, IndexNames.IBEX35),
    ("COLONIAL", StockCodes.COLONIAL, IndexNames.IBEX35),
    ("DIA", StockCodes.DIA, IndexNames.IBEX35),
    ("ENAGAS", StockCodes.ENAGAS, IndexNames.IBEX35),
    ("ENDESA", StockCodes.ENDESA, IndexNames.IBEX35),
    ("FERROVIAL", StockCodes.FERROVIAL, IndexNames.IBEX35),
    ("GAS_NATURAL", StockCodes.GAS_NATURAL, IndexNames.IBEX35),
    ("GRIFOLS", StockCodes.GRIFOLS, IndexNames.IBEX35),
    ("IAG", StockCodes.IAG, IndexNames.IBEX35),
    ("IBERDROLA", StockCodes.IBERDROLA, IndexNames.IBEX35),
    ("INDITEX", StockCodes.INDITEX, IndexNames.IBEX35),
    ("INDRA", StockCodes.INDRA, IndexNames.IBEX35),
    ("MAPFRE", StockCodes.MAPFRE, IndexNames.IBEX35),
    ("MEDIASET", StockCodes.MEDIASET, IndexNames.IBEX35),
    ("MELIA_HOTELS", StockCodes.MELIA_HOTELS, IndexNames.IBEX35),
    ("MERLIN_PROP", StockCodes.MERLIN_PROP, IndexNames.IBEX35),
    ("RED_ELECTRICA", StockCodes.RED_ELECTRICA, IndexNames.IBEX35),
    ("REPSOL", StockCodes.REPSOL, IndexNames.IBEX35),
    ("SANTANDER", StockCodes.SANTANDER, IndexNames.IBEX35),
    ("SIEMENS_GAMESA", StockCodes.SIEMENS_GAMESA, IndexNames.IBEX35),
    ("TECNICAS_REUNIDAS", StockCodes.TECNICAS_REUNIDAS, IndexNames.IBEX35),
    ("TELEFONICA", StockCodes.TELEFONICA, IndexNames.IBEX35),
    ("VISCOFA", StockCodes.VISCOFAN, IndexNames.IBEX35),
    ("BME", StockCodes.BME, None)
])

NASDAQ = Market(MarketNames.NASDAQ, [
    ("FACEBOOK", StockCodes.FACEBOOK, None),
    ("GOOGLE", StockCodes.GOOGLE, None),
    ("APPLE", StockCodes.APPLE, None),
    ("AMAZON", StockCodes.AMAZON, None),
    ("NVIDIA", StockCodes.NVIDIA, None),
    ("NETFLIX", StockCodes.NETFLIX, None),
    ("INTEL", StockCodes.INTEL, None),
    ("MICROSOFT", StockCodes.MICROSOFT, None),
    ("PAYPAL", StockCodes.PAYPAL, None),
    ("CISCO", StockCodes.CISCO, None),
    ("TESLA", StockCodes.TESLA, None),
])

NYSE = Market(MarketNames.NYSE, [
    ("TWITTER", StockCodes.TWITTER, None),
    ("ALIBABA", StockCodes.ALIBABA, None),
    ("JP_MORGAN", StockCodes.JP_MORGAN, None),
    ("NIKE", StockCodes.NIKE, None),
    ("IBM", StockCodes.IBM, None),
    ("VISA", StockCodes.VISA, None),
    ("MCDONALDS", StockCodes.MCDONALDS, None),
    ("ORACLE", StockCodes.ORACLE, None),
    ("COCA_COLA", StockCodes.COCA_COLA, None),
    ("WALT_DISNEY", StockCodes.WALT_DISNEY, None),
    ("MATERCARD", StockCodes.MATERCARD, None),
    ("GENERAL_MOTORS", StockCodes.GENERAL_MOTORS, None),
    ("JOHNSON_JOHNSON", StockCodes.JOHNSON_JOHNSON, None),
    ("FORD", StockCodes.FORD, None),
    ("DELTA_AIRLINES", StockCodes.DELTA_AIRLINES, None),
    ("WALMART", StockCodes.WALMART, None),
    ("CITI_GROUP", StockCodes.CITI_GROUP, None),
    ("CHEVRON", StockCodes.CHEVRON, None),
    ("BANK_OF_AMERICA", StockCodes.BANK_OF_AMERICA, None),
    ("3M", StockCodes._3M, None),
])

def get_data(stocks):
    data = []
    for stock in stocks:
        print("Getting data for stock %s" % stock.name)
        try:
            if stock.market.name in finviz.AVAILABLE_MARKETS:
                print("Finviz api")
                stock_result = finviz.api(stock)
            else:
                print("Expansion api")
                stock_result = expansion.api(stock)

            try:
                if stock.market.name in yahoo.AVAILABLE_MARKETS:
                    print("Yahoo api")
                    additional_info = yahoo.api(stock)
                    price = stock_result["value"]
                    yahoo_price = additional_info["value"]

                    if price == yahoo_price:
                        # Merge data
                        fundamental_analysis = stock_result["fundamental_analysis"]
                        yahoo_fundamental_analysis = additional_info["fundamental_analysis"]
                        expected_price = (fundamental_analysis["expected_price"] + yahoo_fundamental_analysis["expected_price"])/2
                        potential = (expected_price - price) * 100 / price

                        fundamental_analysis["expected_price"] = expected_price
                        fundamental_analysis["potential"] = potential
                        fundamental_analysis["growth_current_year"] = yahoo_fundamental_analysis["growth_current_year"]
                        fundamental_analysis["growth_next_year"] = yahoo_fundamental_analysis["growth_next_year"]
                        fundamental_analysis["growth_next_five_year"] = yahoo_fundamental_analysis["growth_next_five_year"]
                    else:
                        print("Mismatch value %s <> %s" % (price, yahoo_price))
            except Exception as e:
                print(e)

            data.append(
                stock_result
            )
        except Exception as e:
            print(e)
            print("Error with stock %s" % stock.name)
    return data
