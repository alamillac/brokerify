from flask import current_app
from flask import request
from flask_restful import Resource
from web.api.views.security import login_required
from modules.logger import context
from app.models.core import Stock
from web.api.serializer import StockHistoricalSchema


class StockResource(Resource):
    @login_required
    def get(self, stock_id=None):
        context.update_uuid()
        if stock_id:
            current_app.logger.debug("Showing stock %s", stock_id)
            stock = Stock.get(stock_id).get_data()
            response = StockHistoricalSchema().dump(stock)
            return response.data, 200

        current_app.logger.debug("Showing all stocks")
        stocks = [stock.get_data() for stock in Stock.all()]
        response = StockHistoricalSchema(many=True).dump(stocks)
        return response.data, 200
