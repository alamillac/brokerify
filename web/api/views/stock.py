from flask import current_app
from flask import request
from flask_restful import Resource
from web.api.views.security import login_required
from modules.logger import context
from app.models.core import Stock
from web.api.serializer import StockHistoricalSchema, StockSchema
from web.api.forms import StockHistoricalForm


class StockResource(Resource):
    @login_required
    def get(self, stock_id=None):
        context.update_uuid()
        attributes = ('id', 'name', 'stats', 'market')
        if stock_id:
            current_app.logger.debug("Showing stock %s", stock_id)
            stock = Stock.get(stock_id)
            response = StockSchema(only=attributes).dump(stock)
            return response.data, 200

        current_app.logger.debug("Showing all stocks")
        stocks = Stock.all()
        response = StockSchema(many=True, only=attributes).dump(stocks)
        return response.data, 200


class StockHistoricalResource(Resource):
    @login_required
    def get(self, stock_id=None):
        context.update_uuid()
        form = StockHistoricalForm().load(request.args)
        if form.errors:
            return {"error": "Invalid data", "fields": form.errors}, 400
        date = form.data.get('date')

        attributes = ('id', 'name', 'historical')
        if stock_id:
            current_app.logger.debug("Showing historical stock %s", stock_id)
            stock = Stock.get(stock_id)
            response = StockSchema(context={'date': date}, only=attributes).dump(stock)
            return response.data, 200

        current_app.logger.debug("Showing all historical stocks")
        stocks = Stock.all()
        response = StockSchema(many=True, context={'date':date}, only=attributes).dump(stocks)
        return response.data, 200
