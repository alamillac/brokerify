"""Create Stock data

Revision ID: ef137f148877
Revises: 3415418b52b3
Create Date: 2018-05-21 15:56:08.766455

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
revision = 'ef137f148877'
down_revision = '3415418b52b3'
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

    mres = conn.execute("select id, code from market")
    mresults = mres.fetchall()
    market_map = {m[1]: m[0] for m in mresults}


    op.bulk_insert(stock,
        [
            # BME
            {"name": "ABERTIS", "code": StockCodes.ABERTIS, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "ACCIONA", "code": StockCodes.ACCIONA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "ACERINOX", "code": StockCodes.ACERINOX, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "ACS", "code": StockCodes.ACS, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "AENA", "code": StockCodes.AENA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "AMADEUS_IT_GROUP", "code": StockCodes.AMADEUS_IT_GROUP, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "ARCELORMITTAL", "code": StockCodes.ARCELORMITTAL, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "BANCO_SABADELL", "code": StockCodes.BANCO_SABADELL, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "BANKIA", "code": StockCodes.BANKIA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "BANKINTER", "code": StockCodes.BANKINTER, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "BBVA", "code": StockCodes.BBVA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "CAIXABANK", "code": StockCodes.CAIXABANK, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "CELLNEX_TELECOM", "code": StockCodes.CELLNEX_TELECOM, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "COLONIAL", "code": StockCodes.COLONIAL, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "DIA", "code": StockCodes.DIA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "ENAGAS", "code": StockCodes.ENAGAS, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "ENDESA", "code": StockCodes.ENDESA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "FERROVIAL", "code": StockCodes.FERROVIAL, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "GAS_NATURAL", "code": StockCodes.GAS_NATURAL, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "GRIFOLS", "code": StockCodes.GRIFOLS, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "IAG", "code": StockCodes.IAG, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "IBERDROLA", "code": StockCodes.IBERDROLA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "INDITEX", "code": StockCodes.INDITEX, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "INDRA", "code": StockCodes.INDRA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "MAPFRE", "code": StockCodes.MAPFRE, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "MEDIASET", "code": StockCodes.MEDIASET, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "MELIA_HOTELS", "code": StockCodes.MELIA_HOTELS, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "MERLIN_PROP", "code": StockCodes.MERLIN_PROP, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "RED_ELECTRICA", "code": StockCodes.RED_ELECTRICA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "REPSOL", "code": StockCodes.REPSOL, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "SANTANDER", "code": StockCodes.SANTANDER, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "SIEMENS_GAMESA", "code": StockCodes.SIEMENS_GAMESA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "TECNICAS_REUNIDAS", "code": StockCodes.TECNICAS_REUNIDAS, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "TELEFONICA", "code": StockCodes.TELEFONICA, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "VISCOFAN", "code": StockCodes.VISCOFAN, "market_id": market_map[MarketCodes.BME], "index_id": index_map[IndexCodes.IBEX35]},
            {"name": "BME", "code": StockCodes.BME, "market_id": market_map[MarketCodes.BME], "index_id": None},

            # NASDAQ
            {"name": "FACEBOOK", "code": StockCodes.FACEBOOK, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "GOOGLE", "code": StockCodes.GOOGLE, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "APPLE", "code": StockCodes.APPLE, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "AMAZON", "code": StockCodes.AMAZON, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "NVIDIA", "code": StockCodes.NVIDIA, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "NETFLIX", "code": StockCodes.NETFLIX, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "INTEL", "code": StockCodes.INTEL, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "MICROSOFT", "code": StockCodes.MICROSOFT, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "PAYPAL", "code": StockCodes.PAYPAL, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "CISCO", "code": StockCodes.CISCO, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},
            {"name": "TESLA", "code": StockCodes.TESLA, "market_id": market_map[MarketCodes.NASDAQ], "index_id": None},

            # NYSE
            {"name": "TWITTER", "code": StockCodes.TWITTER, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "ALIBABA", "code": StockCodes.ALIBABA, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "JP_MORGAN", "code": StockCodes.JP_MORGAN, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "NIKE", "code": StockCodes.NIKE, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "IBM", "code": StockCodes.IBM, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "VISA", "code": StockCodes.VISA, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "MCDONALDS", "code": StockCodes.MCDONALDS, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "ORACLE", "code": StockCodes.ORACLE, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "COCA_COLA", "code": StockCodes.COCA_COLA, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "WALT_DISNEY", "code": StockCodes.WALT_DISNEY, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "MATERCARD", "code": StockCodes.MATERCARD, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "GENERAL_MOTORS", "code": StockCodes.GENERAL_MOTORS, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "JOHNSON_JOHNSON", "code": StockCodes.JOHNSON_JOHNSON, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "FORD", "code": StockCodes.FORD, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "DELTA_AIRLINES", "code": StockCodes.DELTA_AIRLINES, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "WALMART", "code": StockCodes.WALMART, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "CITI_GROUP", "code": StockCodes.CITI_GROUP, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "CHEVRON", "code": StockCodes.CHEVRON, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "BANK_OF_AMERICA", "code": StockCodes.BANK_OF_AMERICA, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
            {"name": "3M", "code": StockCodes._3M, "market_id": market_map[MarketCodes.NYSE], "index_id": None},
        ]
    )


def downgrade():
    pass
