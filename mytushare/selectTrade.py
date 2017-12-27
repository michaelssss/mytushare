import datetime as dt

import tushare as ts

import mytushare.tradeInfo as my


# 以二十天均价为准点，偏离均价两个点即可入选
def select(duration):
    stocks = ts.get_stock_basics()
    now = dt.datetime.now()
    before = (dt.datetime.now() - dt.timedelta(days=duration))
    for _, row in stocks.iterrows():
        print("analyze ", row['code'])
        df = ts.get_k_data(code=row['code'], start=before.strftime("%Y-%m-%d"),
                           end=now.strftime("%Y-%m-%d"))
        avgPrice = (my.get_average_open_price_in_duration(df) + my.get_average_close_price_in_duration(df)) / 2
        lastday = (dt.datetime.now() - dt.timedelta(days=1))
        df1 = ts.get_k_data(code=row['code'], start=lastday.strftime("%Y-%m-%d"),
                            end=lastday.strftime("%Y-%m-%d"))
        for _, row1 in df1.iterrows():
            lastdayprice = row1['close']
            offrate = ((lastdayprice - avgPrice) / avgPrice) * 100
            if offrate > 2:
                print(row['code'])


select(5)
