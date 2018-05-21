"""Create Index data

Revision ID: 6acee775d4a7
Revises: eed12e213dd2
Create Date: 2018-05-21 15:12:16.182971

"""
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.sql import table, column
from app.codes import IndexCodes



# revision identifiers, used by Alembic.
revision = '6acee775d4a7'
down_revision = 'bc70c566a457'
branch_labels = None
depends_on = None


def upgrade():
    index = table('index',
        column('name', String),
        column('code', String)
    )
    op.bulk_insert(index,
        [
            {"name": "IBEX35", "code": IndexCodes.IBEX35},
            {"name": "S&P500", "code": IndexCodes.SP500},
            {"name": "NASDAQ100", "code": IndexCodes.NASDAQ100},
            {"name": "Industrial Dow Jones", "code": IndexCodes.DOW_JONES}
        ]
    )


def downgrade():
    pass
