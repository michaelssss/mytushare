import datetime as dt

import tushare as ts

from mytushare import utils as utils


def cal(duration):
    stocks = ts.get_stock_basics()
    now = dt.datetime.now()
    totalOffsetrate = 0
    index = 0
    for stockCode, _ in stocks.iterrows():
        index += 1
        avgPrice = utils.CalcAvg(duration, stockCode)
        lastday = (now - dt.timedelta(days=1))
        df1 = ts.get_k_data(code=stockCode, start=lastday.strftime("%Y-%m-%d"),
                            end=lastday.strftime("%Y-%m-%d"))
        for _, row1 in df1.iterrows():
            lastdayprice = row1['close']
            totalOffsetrate += ((lastdayprice - avgPrice) * 100) / avgPrice
    print("this year all stock avg offsetrate is %.2f%%" % (totalOffsetrate / index))


def main():
    cal(365)
