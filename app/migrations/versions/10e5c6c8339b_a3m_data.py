"""A3M data

Revision ID: 10e5c6c8339b
Revises: e906bb53afd6
Create Date: 2018-05-27 19:14:14.642918

"""
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, Integer
from sqlalchemy.sql import table, column
from app.codes import StockCodes, MarketCodes


# revision identifiers, used by Alembic.
revision = '10e5c6c8339b'
down_revision = 'e906bb53afd6'
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

    mres = conn.execute("select id, code from market")
    mresults = mres.fetchall()
    market_map = {m[1]: m[0] for m in mresults}


    op.bulk_insert(stock,
        [
            {"name": "ATRESMEDIA", "code": StockCodes.ATRESMEDIA, "market_id": market_map[MarketCodes.BME], "index_id": None},
        ]
    )


def downgrade():
    pass
