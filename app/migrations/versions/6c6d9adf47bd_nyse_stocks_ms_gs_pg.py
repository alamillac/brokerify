"""NYSE stocks MS-GS-PG

Revision ID: 6c6d9adf47bd
Revises: ec71f041ff28
Create Date: 2019-01-23 22:39:40.926476

"""
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, Integer
from sqlalchemy.sql import table, column
from app.codes import StockCodes, MarketCodes, IndexCodes


# revision identifiers, used by Alembic.
revision = '6c6d9adf47bd'
down_revision = 'ec71f041ff28'
branch_labels = None
depends_on = None


def upgrade():
    stock = table('stock',
        column('name', String),
        column('code', String),
        column('market_id', Integer),
        column('index_id', Integer)
    )

    conn = op.get_bind()
    ires = conn.execute("select id, code from 'index'")
    iresults = ires.fetchall()
    index_map = {i[1]: i[0] for i in iresults}

    conn = op.get_bind()
    mres = conn.execute("select id, code from market")
    mresults = mres.fetchall()
    market_map = {m[1]: m[0] for m in mresults}


    op.bulk_insert(stock,
        [
            {"name": "Morgan Stanley", "code": StockCodes.MORGAN_STANLEY, "market_id": market_map[MarketCodes.NYSE], "index_id": index_map[IndexCodes.SP500]},
            {"name": "Goldman Sachs", "code": StockCodes.GOLDMAN_SACHS, "market_id": market_map[MarketCodes.NYSE], "index_id": index_map[IndexCodes.SP500]},
            {"name": "Procter & Gamble", "code": StockCodes.PROCTER_AND_GAMBLE, "market_id": market_map[MarketCodes.NYSE], "index_id": index_map[IndexCodes.SP500]},
        ]
    )

def downgrade():
    pass
