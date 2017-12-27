import datetime as dt
import sys

import tushare as ts


# 以二十天均价为准点，偏离均价两个点即可入选
def select(duration, offsetrate):
    stocks = ts.get_stock_basics()
    now = dt.datetime.now()
    before = (dt.datetime.now() - dt.timedelta(days=duration))
    for stockCode, row in stocks.iterrows():
        # print("analyze name=", row['name'], " code=", stockCode)
        df = ts.get_k_data(code=stockCode, start=before.strftime("%Y-%m-%d"),
                           end=now.strftime("%Y-%m-%d"))
        avgPrice = (get_average_open_price_in_duration(df) + get_average_close_price_in_duration(df)) / 2
        lastday = (dt.datetime.now() - dt.timedelta(days=1))
        df1 = ts.get_k_data(code=stockCode, start=lastday.strftime("%Y-%m-%d"),
                            end=lastday.strftime("%Y-%m-%d"))
        for _, row1 in df1.iterrows():
            lastdayprice = row1['close']
            offrate = ((lastdayprice - avgPrice) / avgPrice) * 100
            if offrate < offsetrate:
                print('buy name=', row['name'], " code=", stockCode, " offsetrate=%.2f%%" % offrate)


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


def main():
    select(int(sys.argv[1]), float(sys.argv[2]))


if __name__ == "__main__":
    main()
