from marshmallow import Schema, fields


class IndexSchema(Schema):
    id = fields.Integer()
    code = fields.Str()
    name = fields.Str()


class MarketSchema(Schema):
    id = fields.Integer()
    code = fields.Str()
    name = fields.Str()
    currency = fields.Str()


class StockSchema(Schema):
    id = fields.Integer()
    code = fields.Str()
    name = fields.Str()
    market = fields.Nested(MarketSchema)
    index = fields.Nested(IndexSchema)


class PortfolioSchema(Schema):
    created_at = fields.DateTime()
    name = fields.Str()
    currency = fields.Str()
    sell_tax = fields.Float()
    dividend_tax = fields.Float()
    id = fields.Integer()
    value = fields.Float()
    initial_value = fields.Float()
    valorization = fields.Float()
    stocks_value = fields.Float()
    dividends = fields.Float()


class UserSchema(Schema):
    username = fields.Str()
    name = fields.Str()
    lastname = fields.Str()
    created_at = fields.DateTime()
    portfolios = fields.Nested(PortfolioSchema, many=True)


class PortfolioStockSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    portfolio = fields.Nested(PortfolioSchema, only='name')
    stock = fields.Nested(StockSchema, only='name')
    type = fields.Str()
    date = fields.Date()
    num_stocks = fields.Integer()
    price = fields.Float()
    commission_price = fields.Float()
    exchange_rate = fields.Float()


class PortfolioDividendSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    portfolio = fields.Nested(PortfolioSchema, only='name')
    stock = fields.Nested(StockSchema, only='name')
    date = fields.Date()
    value = fields.Float()
