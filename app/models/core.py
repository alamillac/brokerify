import logging
import datetime
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, func, ForeignKey, Index as IndexColumn
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from app import settings

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

    @classmethod
    def get(cls, code):
        return db_session.query(cls).filter(cls.code == code).one_or_none()

    @classmethod
    def all(cls):
        return db_session.query(cls).all()


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
        db_engine.execute(cls.__table__.insert(), items)
