from flask import Flask
from sqlalchemy import insert

from dl_modeling.app.model.predict import predict
from dl_modeling.app.preprocess.preprocessing import make_batch, process_raw_data
from dl_modeling.app.preprocess.get_data import get_recent_data
from dl_modeling.app.preprocess.maria_candle_entity import MariaCandles
from dl_modeling.app.preprocess.get_engine import maria


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def post_predict():
    data = get_recent_data()
    data = process_raw_data(data)
    markets, batch_data = make_batch(data)
    pred = predict(batch_data, markets)

    insert_datas = []
    for pk, value in pred.items():
        market, utc, open, high, low, close, value, volume = pk
        insert_data ={
            'market': market,
            'candle_date_time_utc': utc,
            'opening_price': open,
            'high_price': high,
            'low_price': low,
            'trade_price': close,
            'candle_acc_trade_price': value,
            'candle_acc_trade_volume': volume,
            'predict': value
        }
        insert_datas.append(insert_data)
    
    with maria.connect() as conn:
        conn.execute(insert(MariaCandles), insert_datas)
        conn.commit()
    return 1

        

    


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
