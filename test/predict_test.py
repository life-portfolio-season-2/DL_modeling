import unittest
from dl_modeling.app.model.predict import predict
from dl_modeling.app.preprocess.preprocessing import make_batch, process_raw_data
from dl_modeling.app.preprocess.get_data import get_recent_data

class PredictTest(unittest.TestCase):
    def test_predict(self):
        data = get_recent_data()
        data = process_raw_data(data)
        markets, batch_data = make_batch(data)
        pred = predict(batch_data, markets)
        print(pred)
