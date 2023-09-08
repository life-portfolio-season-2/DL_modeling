import unittest
from dl_modeling.app.preprocess.get_data import get_recent_data

class GetDataTest(unittest.TestCase):
    def test_get_recent_date(self):
        data = get_recent_data()
        print(data)