import logging
import app.api.expansion
import app.api.yahoo
import app.api.finviz
import app.api.wall_street_journal
import app.api.eleconomista


logger = logging.getLogger("Api")

def merge(to_merge, from_merge, keys, force=True):
    for key in keys:
        if key not in to_merge:
            logger.warning("Merging invalid key: %s", key)
            continue

        if to_merge[key] and not force:
            continue

        if not from_merge[key]:
            continue
        to_merge[key] = from_merge[key]


def get_data(stocks):
    data = []
    for stock in stocks:
        logger.info("Getting data for stock %s" % stock.name)
        try:
            if stock.market.code in finviz.AVAILABLE_MARKETS:
                logger.info("Finviz api")
                stock_result = finviz.api(stock)
            else:
                logger.info("Expansion api")
                stock_result = expansion.api(stock)

            try:
                if stock.market.code in yahoo.AVAILABLE_MARKETS:
                    logger.info("Yahoo api")
                    additional_info = yahoo.api(stock)

                    # Merge data
                    merge(stock_result, additional_info, ["value", "volume", "mean_volume_60", "max_52", "min_52", "dividend_yield"])
                    merge(stock_result["ratios"], additional_info["ratios"], ["bpa", "per"], force=False)

                    price = stock_result["value"]
                    fundamental_analysis = stock_result["fundamental_analysis"]
                    yahoo_fundamental_analysis = additional_info["fundamental_analysis"]
                    if fundamental_analysis["expected_price"]:
                        expected_price = (fundamental_analysis["expected_price"] + yahoo_fundamental_analysis["expected_price"])/2
                    else:
                        expected_price = yahoo_fundamental_analysis["expected_price"]
                    potential = (expected_price - price) * 100 / price

                    fundamental_analysis["expected_price"] = expected_price
                    fundamental_analysis["potential"] = potential
                    fundamental_analysis["growth_current_year"] = yahoo_fundamental_analysis["growth_current_year"]
                    fundamental_analysis["growth_next_year"] = yahoo_fundamental_analysis["growth_next_year"]
                    fundamental_analysis["growth_next_five_year"] = yahoo_fundamental_analysis["growth_next_five_year"]
            except Exception as e:
                logger.exception(e)

            data.append(
                stock_result
            )
        except Exception as e:
            logger.exception(e)
            logger.error("Error with stock %s" % stock.name)
    return data


def get_index_data(indices, start_date, end_date):
    data = []
    for index in indices:
        try:
            if index.code in wall_street_journal.AVAILABLE_INDEX:
                logger.info("Wall street journal api")
                result = wall_street_journal.api(index.code, start_date, end_date)
            elif index.code in eleconomista.AVAILABLE_INDEX:
                logger.info("El economista api")
                result = eleconomista.api(index.code, start_date, end_date)
            else:
                logger.warning("Index %s not found", index.name)
                continue
            data += result
        except Exception as e:
            logger.exception(e)
            logger.error("Error with index %s" % index.name)
    return data
