import datetime as dt
import sys

import tushare as ts


# 如果近duration的均值偏离值小于offsetrate且近duration2均值偏离值大于offsetrate2则入选
def select(duration, offsetrate, duration2, offsetrate2):
    with open("/root/pythonTrade/result", "a+") as file:
        stocks = ts.get_stock_basics()
        now = dt.datetime.now()
        before = (dt.datetime.now() - dt.timedelta(days=duration))
        before2 = (dt.datetime.now() - dt.timedelta(days=duration2))
        file.writelines(now.strftime("%Y-%m-%d %H:%M%S"))
        for stockCode, row in stocks.iterrows():
            # print("analyze name=", row['name'], " code=", stockCode)
            df = ts.get_k_data(code=stockCode, start=before.strftime("%Y-%m-%d"),
                               end=now.strftime("%Y-%m-%d"))
            avgPrice = (get_average_open_price_in_duration(df) + get_average_close_price_in_duration(df)) / 2
            df2 = ts.get_k_data(code=stockCode, start=before2.strftime("%Y-%m-%d"),
                                end=now.strftime("%Y-%m-%d"))
            avgPrice2 = (get_average_open_price_in_duration(df2) + get_average_close_price_in_duration(df2)) / 2

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
    select(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))


if __name__ == "__main__":
    main()
