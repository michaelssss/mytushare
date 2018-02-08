import datetime
import time

import tushare as ts

import db.DBConnection as db1


class Relatetion:
    def __init__(self, code1, code2, re):
        self.code1 = code1
        self.code2 = code2
        self.relation = re


# 将数据存入本地
def selectIntoLocal(offdate):
    now = datetime.datetime.now()
    start = (now - datetime.timedelta(days=offdate)).strftime('%Y-%m-%d')
    end = now.strftime('%Y-%m-%d')
    stocks = ts.get_stock_basics()
    for stockCode, row in stocks.iterrows():
        while True:
            try:
                df = ts.get_h_data(code=stockCode, start=start, end=end, pause=5)
                df.insert(0, 'code', stockCode)
                insertDB(df)
                break
            except IOError:
                print("get_h_data wrong sleep " + str(10 * 60) + "second")
                time.sleep(10 * 60)


def insertDB(df):
    for index, row in df.iterrows():
        sql = "insert into DATA.h_data(`code`,`date`,`open`,`high`,`close`,`low`,`volume`,`amount`) values('%s','%s','%f','%f','%f','%f','%s','%s'); " % (
            row['code'], index, row['open'], row['high'], row['close'], row['low'], row['volume'], row['amount'])
        db1.cursor.execute(sql)
        db1.db.commit()


def main(duration):
    selectIntoLocal(int(duration))
