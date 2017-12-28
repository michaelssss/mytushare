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
    with open("/root/pythonTrade/result", "a+") as file:
        file.writelines(now.strftime("%Y-%m-%d %H:%M:%S\r\n"))
        file.write("during {0} days all stock avg offsetrate is {1:.2f}%".format(duration, totalOffsetrate / index))


def main(duration):
    cal(int(duration))
