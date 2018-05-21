"""Create Market data

Revision ID: 3415418b52b3
Revises: 6acee775d4a7
Create Date: 2018-05-21 15:52:35.513877

"""
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.sql import table, column
from app.codes import MarketCodes


# revision identifiers, used by Alembic.
revision = '3415418b52b3'
down_revision = '6acee775d4a7'
branch_labels = None
depends_on = None


def upgrade():
    market = table('market',
        column('name', String),
        column('code', String)
    )
    op.bulk_insert(market,
        [
            {"name": "BME", "code": MarketCodes.BME},
            {"name": "NASDAQ", "code": MarketCodes.NASDAQ},
            {"name": "NYSE", "code": MarketCodes.NYSE}
        ]
    )


def downgrade():
    pass
