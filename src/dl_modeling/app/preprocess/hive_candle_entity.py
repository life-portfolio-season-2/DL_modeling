from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import TIMESTAMP, Integer, String, DateTime,Double
from sqlalchemy.schema import Column

from .get_engine import hive

Base = declarative_base()

class HiveCandles(Base):
    __tablename__ = 'min_chart'

    market = Column(String, nullable=False, primary_key=True)
    candle_date_time_utc = Column(DateTime, nullable=False, primary_key=True)
    candle_date_time_kst = Column(DateTime, nullable=False)
    timestamp_column = Column(TIMESTAMP, nullable=False)
    opening_price = Column(Double, nullable=False)
    high_price = Column(Double, nullable=False)
    low_price = Column(Double, nullable=False)
    trade_price = Column(Double, nullable=False)
    candle_acc_trade_price = Column(Double, nullable=False)
    candle_acc_trade_volume = Column(Double, nullable=False)
    unit = Column(Integer, nullable=False)



HiveCandles.__table__.create(bind=hive, checkfirst=True)