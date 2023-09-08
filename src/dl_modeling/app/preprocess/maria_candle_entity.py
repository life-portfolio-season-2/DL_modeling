from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Double, String, DateTime, Float
from sqlalchemy.schema import Column

from .get_engine import maria

Base = declarative_base()

class MariaCandles(Base):
    __tablename__ = 'candles'

    market = Column(String(10), nullable=False, primary_key=True)
    candle_date_time_utc = Column(DateTime, nullable=False, primary_key=True)
    opening_price = Column(Double, nullable=False)
    high_price = Column(Double, nullable=False)
    low_price = Column(Double, nullable=False)
    trade_price = Column(Double, nullable=False)
    candle_acc_trade_price = Column(Double, nullable=False)
    candle_acc_trade_volume = Column(Double, nullable=False)
    predict = Column(Float, nullable=True)

MariaCandles.__table__.create(bind=maria, checkfirst=True)