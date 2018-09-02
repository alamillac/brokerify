from marshmallow import Schema, fields


class IndexSchema(Schema):
    id = fields.Integer()
    code = fields.Str()
    name = fields.Str()
    value = fields.Float()
    valorization_one_day = fields.Float()
    valorization_one_week = fields.Float()
    valorization_one_year = fields.Float()


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


class StockHistoricalSchema(Schema):
    stock = fields.Nested(StockSchema, only=('id', 'name', 'market'))
    date = fields.Date()
    price = fields.Float()
    expected_price = fields.Float()
    max_52 = fields.Float()
    per = fields.Float()
    growth_next_year = fields.Float()
    growth_next_five_year = fields.Float()
    dividend_yield = fields.Float()
    approx_valorization = fields.Float()
    potential = fields.Float()
    fixed_potential = fields.Float()
