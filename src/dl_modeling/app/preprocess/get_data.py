from .get_engine import maria_session, hive_session
from .hive_candle_entity import HiveCandles
from .maria_candle_entity import MariaCandles

from sqlalchemy import Row, select
from sqlalchemy.sql.expression import func
from datetime import datetime, timedelta


def get_recent_data():
    with maria_session as s:
        recent_datetime = s.scalar(select(func.max(MariaCandles.candle_date_time_utc)))

    recent_datetime = recent_datetime or datetime(year=2017,month=1, day=1)

    stmt = select(HiveCandles.market, 
                HiveCandles.candle_acc_trade_price, 
                HiveCandles.candle_acc_trade_volume, 
                HiveCandles.candle_date_time_utc, 
                HiveCandles.high_price, 
                HiveCandles.low_price, 
                HiveCandles.opening_price, 
                HiveCandles.trade_price) \
            .where(HiveCandles.candle_date_time_utc > recent_datetime)\
            .distinct(HiveCandles.market, HiveCandles.candle_date_time_utc)

    with hive_session as s:
        raw_data:list[Row] = s.execute(stmt).all()

    return raw_data

