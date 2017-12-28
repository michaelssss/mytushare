import datetime as dt

import tushare as ts

import mytushare.utils as utils


# 如果近duration的均值偏离值小于offsetrate且近duration2均值偏离值大于offsetrate2则入选
def select(duration, offsetrate, duration2, offsetrate2):
    with open("/root/pythonTrade/result", "a+") as file:
        stocks = ts.get_stock_basics()
        now = dt.datetime.now()
        file.writelines(now.strftime("%Y-%m-%d %H:%M:%S \r\n"))
        for stockCode, row in stocks.iterrows():
            avgPrice, = utils.CalcAvg(duration, stockCode)
            avgPrice2 = utils.CalcAvg(duration2, stockCode)
            lastday = (dt.datetime.now() - dt.timedelta(days=1))
            df1 = ts.get_k_data(code=stockCode, start=lastday.strftime("%Y-%m-%d"),
                                end=lastday.strftime("%Y-%m-%d"))
            for _, row1 in df1.iterrows():
                lastdayprice = row1['close']
                offrate = ((lastdayprice - avgPrice) / avgPrice) * 100
                offrate2 = ((lastdayprice - avgPrice2) / avgPrice2) * 100
                if offrate < offsetrate and offrate2 > offsetrate2:
                    file.write(
                        str.format("name={0}, code={1}, offsetrate={2:.2f}%  ,offsetrate2={3:.2f}% \r\n", row['name'],
                                   stockCode, offrate, offrate2))
                    file.flush()


def main(duration, offsetrate, duration2, offsetrate2):
    select(duration, offsetrate, duration2, offsetrate2)
