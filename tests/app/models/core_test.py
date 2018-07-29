import unittest
import datetime
import app.models.core as db
from app.codes import IndexCodes


class TestDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.init('sqlite:///:memory:')
        db.TableBase.metadata.create_all(db.db_engine)


class TestIndex(TestDB):
    def test_get_return_from_date(self):
        ibex35 = db.Index()
        ibex35.name = "IBEX35"
        ibex35.code = IndexCodes.IBEX35
        db.add(ibex35)

        prices = [{
            "name": ibex35.name,
            "date": datetime.date(2018, 1, 1),
            "open": 1.0,
            "high": 2.0,
            "low": 0.5,
            "close": 2.0
        },{
            "name": ibex35.name,
            "date": datetime.date(2018, 1, 2),
            "open": 2.0,
            "high": 4.0,
            "low": 2.5,
            "close": 4.0
        },{
            "name": ibex35.name,
            "date": datetime.date(2018, 1, 3),
            "open": 3.0,
            "high": 4.0,
            "low": 2.5,
            "close": 2.0
        },{
            "name": ibex35.name,
            "date": datetime.date(2018, 1, 4),
            "open": 2.0,
            "high": 5.0,
            "low": 1.5,
            "close": 1.5
        }]

        db.IndexHistoricalPrices.bulk_insert(prices)

        expected_result = [{
            "return": 1,
            "date": datetime.date(2018, 1, 1)
        },{
            "return": 2,
            "date": datetime.date(2018, 1, 2)
        },{
            "return": 1,
            "date": datetime.date(2018, 1, 3)
        },{
            "return": 0.75,
            "date": datetime.date(2018, 1, 4)
        }]
        result = ibex35.get_return_from_date()
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
