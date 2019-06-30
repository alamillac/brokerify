import datetime
from marshmallow import Schema, fields, validates, ValidationError
from app.models.core import PortfolioStock


class UserStockForm(Schema):
    portfolio_id = fields.Integer(required=True)
    stock_id = fields.Integer(required=True)
    type = fields.Method(required=True, deserialize='load_type')
    date = fields.DateTime(required=True, format="%Y-%m-%d")
    num_stocks = fields.Integer(required=True)
    price = fields.Float(required=True)
    commission_price = fields.Float(required=True)

    def load_type(self, value):
        if value.lower() == "buy":
            return PortfolioStock.Type.BUY
        if value.lower() == "sell":
            return PortfolioStock.Type.SELL
        return None

    @validates('type')
    def validate_type(self, value):
        if value not in [PortfolioStock.Type.BUY, PortfolioStock.Type.SELL]:
            raise ValidationError("Invalid type. It should be 'buy' or 'sell'")


class LoginForm(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class StockHistoricalForm(Schema):
    date = fields.DateTime(required=False, format="%Y-%m-%d")
