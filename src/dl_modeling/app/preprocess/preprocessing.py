from sqlalchemy import Row
from .hive_candle_entity import HiveCandles
from .hive_dto import HiveDto
import pandas as pd
from datetime import timedelta
import numpy as np

period = 1
unit = 1
past = 1
C = 7

def process_raw_data(raw_data:list[Row]):
    df_data = [HiveDto(**d._asdict()).to_dict() for d in raw_data]
    df = pd.DataFrame(df_data)
    groupby_df = df.groupby('market')
    output_dfs = {}
    for market, _df in groupby_df:
        # ['market', 'utc', 'open', 'high', 'low', 'close', 'value', 'volume']
        pk = tuple(_df.loc[_df.utc == _df.utc.max(), :].values.tolist()[0])
        _df.drop_duplicates('utc', inplace=True)
        output_dfs[pk] = _df.reset_index().drop(columns=['index', 'market']).set_index('utc')

    return output_dfs


def _scaling(data:pd.DataFrame) -> pd.DataFrame:
    data[['open','high','low','close','value_per_volume']] = data[['open','high','low','close','value_per_volume']].apply(lambda x: x/data.close)
    data[['volume','value']] = data[['volume','value']] / data[['volume','value']].sum()
    data.fillna(0, inplace=True)
    return data

def _preprocess_input_data(data:pd.DataFrame) -> np.ndarray:

    data['value_per_volume'] = data['value'] / data['volume']
    data.loc[data['value_per_volume'].isna(),'value_per_volume'] = data['close']

    rolling_data = data.rolling(f'{(period)}T')
    past_range = [data.index.max() - timedelta(minutes=i)*unit for i in range(past)]

    datas = []
    for d in rolling_data:
        if len(d) == (period) and d.index.max() in past_range:
            d = _scaling(d.copy())
            datas.append(d.values)
    datas = np.stack(datas, axis=0)
    return datas

def make_batch(candles:dict[str,pd.DataFrame]) -> tuple[tuple[str],np.ndarray]:
    pks, datas = zip(*[(pk, _preprocess_input_data(df)) for pk, df in candles.items()])
    batch_data = np.stack(datas, axis=0).reshape([-1,period, C])
    return pks, batch_data