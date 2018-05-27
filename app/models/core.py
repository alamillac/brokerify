import logging
import datetime
import sqlalchemy
from sqlalchemy import create_engine, Column, Enum, Integer, String, Float, Date, DateTime, func, ForeignKey, Index as IndexColumn
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from app import settings
from app.codes import CurrencyCodes
import enum

# Index table

# Stock table

DB_CONF = settings.DATABASE

db_engine = create_engine(DB_CONF['url'], encoding=DB_CONF['encoding'])
db_session = sessionmaker(bind=db_engine, autocommit=True)()

TableBase = declarative_base()

logger = logging.getLogger("CoreDB")


class Index(TableBase):
    __tablename__ = "index"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, index=True, unique=True)
    name = Column(String(100), nullable=False)

    @classmethod
    def get(cls, code):
        return db_session.query(cls).filter(cls.code == code).one_or_none()

    @classmethod
    def all(cls):
        return db_session.query(cls).all()

    def get_return_from_date(self, date=None):
        if date:
            historical_prices = db_session.query(IndexHistoricalPrices).filter(
                IndexHistoricalPrices.index_id == self.id,
                IndexHistoricalPrices.date >= date
            ).order_by(IndexHistoricalPrices.date).all()
        else:
            historical_prices = db_session.query(IndexHistoricalPrices).filter(
                IndexHistoricalPrices.index_id == self.id
            ).order_by(IndexHistoricalPrices.date).all()
        if not historical_prices:
            return []
        fp = historical_prices[0] # First price
        return [{"date": hi.date, "return": hi.close_price/fp.close_price} for hi in historical_prices]


class Market(TableBase):
    __tablename__ = "market"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, index=True, unique=True)
    name = Column(String(100), nullable=False)
    currency = Column(String(3), nullable=False)

    @classmethod
    def get(cls, code):
        return db_session.query(cls).filter(cls.code == code).one_or_none()

    @classmethod
    def all(cls):
        return db_session.query(cls).all()


class Stock(TableBase):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, index=True, unique=True)
    name = Column(String(100), nullable=False)
    market_id = Column(Integer, ForeignKey('market.id'), nullable=False)
    index_id = Column(Integer, ForeignKey('index.id'), nullable=True)
    market = relationship('Market')
    index = relationship('Index')

    @property
    def currency(self):
        return self.market.currency

    @classmethod
    def get(cls, code):
        return db_session.query(cls).filter(cls.code == code).one_or_none()

    @classmethod
    def get_by_id(cls, id):
        return db_session.query(cls).filter(cls.id == id).one_or_none()

    @classmethod
    def get_by_name(cls, name):
        return db_session.query(cls).filter(cls.name == name).one_or_none()

    @classmethod
    def all(cls):
        return db_session.query(cls).all()

    def get_return_from_date(self, date=None):
        if date:
            historical_prices = db_session.query(StockHistoricalData).filter(
                StockHistoricalData.stock_id == self.id,
                StockHistoricalData.date >= date
            ).order_by(StockHistoricalData.date).all()
        else:
            historical_prices = db_session.query(StockHistoricalData).filter(
                StockHistoricalData.stock_id == self.id
            ).order_by(StockHistoricalData.date).all()
        if not historical_prices:
            return []
        fp = historical_prices[0] # First price
        return [{"date": hi.date, "return": hi.price/fp.price} for hi in historical_prices]

    def get_data(self):
        return db_session.query(StockHistoricalData).filter(
            StockHistoricalData.stock_id == self.id
        ).order_by(StockHistoricalData.date.desc()).first()


class IndexHistoricalPrices(TableBase):
    __tablename__ = "index_prices"
    __table_args__ = (
        IndexColumn(
            'index_date_unique',
            'date',
            'index_id',
            unique=True
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    import_date = Column(DateTime, nullable=False, default=func.now)
    date = Column(Date, nullable=False)
    index_id = Column(Integer, ForeignKey('index.id'), nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    index = relationship("Index")

    @classmethod
    def get(cls, index_code, date):
        index = Index.get(index_code)
        return db_session.query(cls).filter(cls.index_id == index.id, cls.date == date).one_or_none()

    @classmethod
    def bulk_insert(cls, index_prices):
        if not index_prices:
            logger.info("Nothing to save in IndexHistoricalPrices")
            return

        items = []
        now = datetime.datetime.now()
        for index_data in index_prices:
            index = Index.get(index_data["name"])
            if not index:
                logger.error("Index %s not found" % index_data["name"])
                continue

            items.append({
                "import_date": now,
                "index_id": index.id,
                "date": index_data["date"],
                "open_price": index_data["open"],
                "high_price": index_data["high"],
                "low_price": index_data["low"],
                "close_price": index_data["close"]
            })
        db_engine.execute(cls.__table__.insert(), items)


class StockHistoricalData(TableBase):
    __tablename__ = "stock_data"
    __table_args__ = (
        IndexColumn(
            'stock_date_unique',
            'date',
            'stock_id',
            unique=True
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    import_date = Column(DateTime, nullable=False, default=func.now)
    date = Column(Date, nullable=False)
    stock_id = Column(Integer, ForeignKey('stock.id'), nullable=False)
    price = Column(Float, nullable=False)
    expected_price = Column(Float, nullable=False)
    max_52 = Column(Float, nullable=False)
    per = Column(Float, nullable=False)
    growth_next_year = Column(Float, nullable=False)
    growth_next_five_year = Column(Float, nullable=False)
    dividend_yield = Column(Float, nullable=False, default=0)
    stock = relationship("Stock")

    @property
    def approx_valorization(self):
        if self.growth_next_five_year:
            return self.fixed_potential*0.5 + self.growth_next_five_year*0.2 + self.dividend_yield*0.3
        else:
            return self.fixed_potential*0.7 + self.dividend_yield*0.3

    @property
    def potential(self):
        return (self.expected_price - self.price) * 100 / self.price

    @property
    def fixed_potential(self):
        if self.expected_price:
            expected_price = self.expected_price
        else:
            expected_price = self.max_52 * 0.85
        expected_price_fixed = min(
            expected_price,
            (self.expected_price + self.max_52)/2
        )
        return (expected_price_fixed - self.price) * 100 / self.price

    @classmethod
    def bulk_insert(cls, stock_data):
        if not stock_data:
            logger.info("Nothing to save in StockHistoricalData")
            return

        now = datetime.datetime.now()
        items = []
        for d in stock_data:
            stock = Stock.get(d["code"])
            if not stock:
                logger.error("Stock %s not found" % d["code"])
                continue

            items.append({
                "import_date": now,
                "date": d["date"],
                "stock_id": stock.id,
                "price": d["value"],
                "expected_price": d["fundamental_analysis"]["expected_price"],
                "max_52": d["max_52"],
                "per": d["ratios"]["per"],
                "growth_next_year": d["fundamental_analysis"]["growth_next_year"],
                "growth_next_five_year": d["fundamental_analysis"]["growth_next_five_year"],
                "dividend_yield": d["dividend_yield"]
            })
        try:
            db_engine.execute(cls.__table__.insert(), items)
        except sqlalchemy.exc.IntegrityError:
            for item in items:
                stock = Stock.get_by_id(item["stock_id"])
                instance = cls.get(stock.code, item["date"])
                instance.price = item["price"]
                instance.expected_price = item["expected_price"]
                instance.max_52 = item["max_52"]
                instance.per = item["per"]
                instance.growth_next_year = item["growth_next_year"]
                instance.growth_next_five_year = item["growth_next_five_year"]
                instance.dividend_yield = item["dividend_yield"]
                db_session.add(instance)
            db_session.flush()

    @classmethod
    def get(cls, stock_code, date):
        stock = Stock.get(stock_code)
        return db_session.query(cls).filter(cls.stock_id == stock.id, cls.date == date).one_or_none()

    @classmethod
    def get_or_create(cls, data):
        if not data:
            logger.info("Null data received")
            return

        stock = Stock.get(data["code"])
        if not stock:
            logger.error("Stock %s not found" % data["code"])
            return
        instance = cls.get(stock.code, data["date"])

        if instance:
            return instance

        del data["code"]
        data["stock_id"] = stock.id
        instance = cls(**data)
        instance.import_date = datetime.datetime.now()
        db_session.add(instance)
        db_session.flush()
        return instance

    def __repr__(self):
        return "%s: price(%.2f) per(%.2f) growth(%.2f) dividend(%.2f) potential(%.2f) valorization(%.2f)" % (self.stock.name, self.price, self.per, self.growth_next_five_year, self.dividend_yield, self.potential, self.approx_valorization)


class User(TableBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now)
    updated_at = Column(DateTime, nullable=False)
    username = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)


class Portfolio(TableBase):
    __tablename__ = "portfolio"
    __table_args__ = (
        IndexColumn(
            'name_user_unique',
            'user_id',
            'name',
            unique=True
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now)
    updated_at = Column(DateTime, nullable=False)
    name = Column(String(100), nullable=False)
    currency = Column(String(3), nullable=False, default=CurrencyCodes.EUR)
    objective_id = Column(Integer, ForeignKey('portfolio_objective.id'), nullable=True)
    sell_tax = Column(Float, nullable=False, default=0.19)
    dividend_tax = Column(Float, nullable=False, default=0.19)

    objective = relationship('Objective')
    user = relationship('User')

    @property
    def price(self):
        return 0  # TODO

    @property
    def risk(self):
        return 0  # TODO 14% volatilidad
    # TODO Diversificación (por fecha, por sector, por pais, por moneda)
    # TODO Rentabilidad (1mes, 3meses, 1año, desde inicio, etc) %, Tendencia %, Ratio Sharpe, VaR 95% anual -23,00%
    # TODO Dividendos

    @classmethod
    def get(cls, user_id, name):
        return db_session.query(cls).filter(cls.user_id == user_id, name == name).one_or_none()

    @classmethod
    def get_or_create(cls, data):
        if not data:
            logger.info("Null data received")
            return

        protfolio = Protfolio.get(data["code"])
        if not stock:
            logger.error("Stock %s not found" % data["code"])
            return
        instance = cls.get(stock.code, data["date"])

        if instance:
            return instance

        del data["code"]
        data["stock_id"] = stock.id
        instance = cls(**data)
        instance.import_date = datetime.datetime.now()
        db_session.add(instance)
        db_session.flush()
        return instance


class PortfolioStock(TableBase):
    __tablename__ = "portfolio_stock"

    class Type(enum.Enum):
        BUY = 0
        SELL = 1

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now)
    updated_at = Column(DateTime, nullable=False)
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'), nullable=False)
    stock_id = Column(Integer, ForeignKey('stock.id'), nullable=False)
    type = Column(Enum(Type), nullable=False)
    date = Column(Date, nullable=False)
    num_stocks = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    commission_price = Column(Float, nullable=False)
    exchange_rate = Column(Float, nullable=False, default=1)

    stock = relationship('Stock')

    @property
    def currency(self):
        return self.stock.currency


class PortfolioObjective(TableBase):
    __tablename__ = "portfolio_objective"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now)
    updated_at = Column(DateTime, nullable=False)
    name = Column(String(100), nullable=False)
    initial_investment = Column(Float, nullable=False)
    monthly_investment = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default=CurrencyCodes.EUR)
    end_date = Column(Date, nullable=False)
    inflation = Column(Float, nullable=False, default=0.03)
    risk = Column(Float, nullable=False, default=0.15)
    taxes = Column(Float, nullable=False, default=0.19)
    expected_return = Column(Float, nullable=False)


class PortfolioDividend(TableBase):
    __tablename__ = "portfolio_dividend"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now)
    updated_at = Column(DateTime, nullable=False)
    stock_id = Column(Integer, ForeignKey('stock.id'), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False) # Gross value

    stock = relationship('Stock')

    @property
    def net_value(self):
        return self.value * (1 - stock.dividend_tax)

    @property
    def currency(self):
        return self.stock.currency
