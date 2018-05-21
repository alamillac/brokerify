import logging
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


class Market(TableBase):
    __tablename__ = "market"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, index=True, unique=True)
    name = Column(String(100), nullable=False)


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
        expected_price_fixed = min(
            self.expected_price,
            (self.expected_price + self.max_52)/2
        )
        return (expected_price_fixed - self.price) * 100 / self.price
