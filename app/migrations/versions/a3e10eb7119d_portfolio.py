"""Portfolio

Revision ID: a3e10eb7119d
Revises: ef137f148877
Create Date: 2018-05-26 00:31:53.935998

"""
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3e10eb7119d'
down_revision = 'ef137f148877'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('portfolio_objective',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('initial_investment', sa.Float(), nullable=False),
    sa.Column('monthly_investment', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('inflation', sa.Float(), nullable=False),
    sa.Column('risk', sa.Float(), nullable=False),
    sa.Column('taxes', sa.Float(), nullable=False),
    sa.Column('expected_return', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('portfolio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('objective_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['objective_id'], ['portfolio_objective.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('portfolio_stock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('portfolio_id', sa.Integer(), nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('BUY', 'SELL', name='type'), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('num_stocks', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('commission_price', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('exchange_rate', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio.id'], ),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('portfolio_stock')
    op.drop_table('portfolio')
    op.drop_table('portfolio_objective')
    # ### end Alembic commands ###