import datetime as dt

import tushare as ts


def get_average_close_price_in_duration(df):
    index = 0
    total = 0
    for _, row in df.iterrows():
        total += row['close']
        index += 1
    if index == 0:
        return 0
    return total / index


def get_average_open_price_in_duration(df):
    index = 0
    total = 0
    for _, row in df.iterrows():
        total += row['open']
        index += 1
    if index == 0:
        return 0
    return total / index


def CalcAvg(duration, stockCode):
    now = dt.datetime.now()
    before = (dt.datetime.now() - dt.timedelta(days=duration))
    df = ts.get_k_data(code=stockCode, start=before.strftime("%Y-%m-%d"),
                       end=now.strftime("%Y-%m-%d"))
    return (get_average_open_price_in_duration(df) + get_average_close_price_in_duration(df)) / 2
