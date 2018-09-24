"""BMW and Ing Bank

Revision ID: ec71f041ff28
Revises: 415118c79ca6
Create Date: 2018-09-24 12:40:46.207699

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
revision = 'ec71f041ff28'
down_revision = '415118c79ca6'
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
            {"name": "Euronext", "code": MarketCodes.EURONEXT, "currency": CurrencyCodes.EUR},
        ]
    )

    conn = op.get_bind()
    mres = conn.execute("select id, code from market")
    mresults = mres.fetchall()
    market_map = {m[1]: m[0] for m in mresults}


    op.bulk_insert(stock,
        [
            {"name": "BMW", "code": StockCodes.BMW, "market_id": market_map[MarketCodes.FRANKFURT], "index_id": None},
            {"name": "ING Groep N.V.", "code": StockCodes.ING_BANK, "market_id": market_map[MarketCodes.EURONEXT], "index_id": None},
        ]
    )


def downgrade():
    pass
