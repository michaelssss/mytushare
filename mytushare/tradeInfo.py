import time as sleeptime

import tushare as ts


class MyStockInfo:
    def __init__(self, stockCode, price):
        self.stockCode = stockCode
        self.holdprice = price


def start(myStock):
    while True:
        for stockinfo in myStock:
            stockbasic = ts.get_realtime_quotes(stockinfo.stockCode)
            for _, row in stockbasic.iterrows():
                nowprice = float(row['ask'])
                holdoffsetrate = ((nowprice - stockinfo.holdprice) / stockinfo.holdprice) * 100
                if holdoffsetrate > 0 and holdoffsetrate > 10:
                    print(row['name'], "sell")
                elif holdoffsetrate < 0 and holdoffsetrate < -5:
                    print(row['name'], "sell")

        sleeptime.sleep(10)


stockinfo = [MyStockInfo(stockCode='000063', price=37.413)]
start(stockinfo)
