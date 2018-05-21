import logging
import app.api.expansion
import app.api.yahoo
import app.api.finviz


logger = logging.getLogger("Api")


def get_data(stocks):
    data = []
    for stock in stocks:
        logger.info("Getting data for stock %s" % stock.name)
        try:
            if stock.market.name in finviz.AVAILABLE_MARKETS:
                logger.info("Finviz api")
                stock_result = finviz.api(stock)
            else:
                logger.info("Expansion api")
                stock_result = expansion.api(stock)

            try:
                if stock.market.name in yahoo.AVAILABLE_MARKETS:
                    logger.info("Yahoo api")
                    additional_info = yahoo.api(stock)
                    price = stock_result["value"]
                    yahoo_price = additional_info["value"]

                    if True:
                    #if price == yahoo_price:
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
                        logger.warning("Mismatch value %s <> %s" % (price, yahoo_price))
            except Exception as e:
                logger.exception(e)

            data.append(
                stock_result
            )
        except Exception as e:
            logger.exception(e)
            logger.error("Error with stock %s" % stock.name)
    return data
