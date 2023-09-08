from dataclasses import dataclass
from datetime import datetime


@dataclass
class HiveDto:
    market:str
    candle_date_time_utc:datetime
    opening_price:float
    high_price:float
    low_price:float
    trade_price:float
    candle_acc_trade_price:float
    candle_acc_trade_volume:float


    def __post_init__(self):
        self.candle_date_time_utc = datetime.strptime(self.candle_date_time_utc, '%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {'market':self.market,
                'utc':self.candle_date_time_utc,
                'open':self.opening_price,
                'high':self.high_price,
                'low':self.low_price,
                'close':self.trade_price,
                'value':self.candle_acc_trade_price,
                'volume':self.candle_acc_trade_volume}