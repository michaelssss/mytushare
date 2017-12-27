import datetime as dt
import time as sleeptime

import tushare as ts


class MyStockInfo:
    def __init__(self, stockCode, price, duration):
        now = dt.datetime.now()
        before = (dt.datetime.now() - dt.timedelta(days=duration))
        df = ts.get_k_data(code=stockCode, start=before.strftime("%Y-%m-%d"),
                           end=now.strftime("%Y-%m-%d"))
        self.stockCode = stockCode
        self.holdprice = price
        self.todayAvgPrice = (get_average_open_price_in_duration(df) + get_average_close_price_in_duration(df)) / 2


def start(myStock):
    while True:
        for stockinfo in myStock:
            stockbasic = ts.get_realtime_quotes(stockinfo.stockCode)
            for _, row in stockbasic.iterrows():
                avgprice = stockinfo.todayAvgPrice
                nowprice = float(row['ask'])
                holdoffsetrate = ((nowprice - stockinfo.holdprice) / stockinfo.holdprice) * 100
                print("avg price=%.2f" % avgprice)
                print("now price=%.2f" % nowprice)
                print("holdoffset rate=%d%%" % (holdoffsetrate * 100))
                if holdoffsetrate > 0 and holdoffsetrate > 10:
                    print(row['name'], "sell")
                    print("avg price=%.2f" % avgprice)
                    print("now price=%.2f" % nowprice)
                    print("holdoffset rate=%d%%" % holdoffsetrate)
        sleeptime.sleep(10)


def get_average_close_price_in_duration(df):
    index = 0
    total = 0
    for _, row in df.iterrows():
        total += row['close']
        index += 1
    return total / index


def get_average_open_price_in_duration(df):
    index = 0
    total = 0
    for _, row in df.iterrows():
        total += row['open']
        index += 1
    return total / index


stockinfo = [MyStockInfo(stockCode='000063', price=37.413, duration=10)]
start(stockinfo)
