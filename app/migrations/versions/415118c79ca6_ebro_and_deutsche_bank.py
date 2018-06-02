"""EBRO and DEUTSCHE_BANK

Revision ID: 415118c79ca6
Revises: 10e5c6c8339b
Create Date: 2018-06-02 21:39:04.827086

"""
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, Integer
from sqlalchemy.sql import table, column
from app.codes import StockCodes, MarketCodes, CurrencyCodes


# revision identifiers, used by Alembic.
revision = '415118c79ca6'
down_revision = '10e5c6c8339b'
branch_labels = None
depends_on = None


def upgrade():
    stock = table('stock',
        column('name', String),
        column('code', String),
        column('market_id', Integer),
        column('index_id', Integer)
    )
    market = table('market',
        column('name', String),
        column('code', String),
        column('currency', String)
    )
    op.bulk_insert(market,
        [
            {"name": "Frankfurt stock exchange", "code": MarketCodes.FRANKFURT, "currency": CurrencyCodes.EUR},
        ]
    )

    conn = op.get_bind()
    mres = conn.execute("select id, code from market")
    mresults = mres.fetchall()
    market_map = {m[1]: m[0] for m in mresults}


    op.bulk_insert(stock,
        [
            {"name": "EBRO", "code": StockCodes.EBRO, "market_id": market_map[MarketCodes.BME], "index_id": None},
            {"name": "Deutsche Bank", "code": StockCodes.DEUTSCHE_BANK, "market_id": market_map[MarketCodes.FRANKFURT], "index_id": None},
        ]
    )


def downgrade():
    pass
