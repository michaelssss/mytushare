import datetime
import time

import tushare as ts

import db.DBConnection as db1
import log.log as logP

SleepTime = 10 * 60
log = logP.log("dataCollection.py")


class Relatetion:
    def __init__(self, code1, code2, re):
        self.code1 = code1
        self.code2 = code2
        self.relation = re


#
#
# offdate : 往前倒多少天
#
#
def getLastStoreDate():
    sql = "select max(dt) from DATA.updatetime;"
    db1.cursor.execute(sql)
    lastDate = db1.cursor.fetchall()
    for date in lastDate:
        return date[0]


def getDuration():
    now = datetime.datetime.now()
    lastUpdate = getLastStoreDate()
    return (now - lastUpdate).days


def selectIntoLocal(offdate):
    now = datetime.datetime.now()
    start = (now - datetime.timedelta(days=offdate)).strftime('%Y-%m-%d')
    end = now.strftime('%Y-%m-%d')
    stocks = ts.get_stock_basics()
    for stockCode, row in stocks.iterrows():
        while True:
            try:
                df = ts.get_h_data(code=stockCode, start=start, end=end, pause=10)
                df.insert(0, 'code', stockCode)
                insertDB(df)
                break
            except IOError:
                log.info("get_h_data wrong sleep " + str(SleepTime) + "second")
                time.sleep(SleepTime)
    log.info("get finish")


def insertDB(df):
    for index, row in df.iterrows():
        # log.info()(index)
        sql = "select * from DATA.h_data as t1 where t1.code='%s' and t1.date='%s'" % (row['code'], index)
        db1.cursor.execute(sql)
        data = db1.cursor.fetchall()
        if len(data) == 0:
            log.info(datetime.datetime.now())
            log.info("insert code=%s,data=%s" % (row['code'], index))
            sql = "replace into DATA.h_data(`code`,`date`,`open`,`high`,`close`,`low`,`volume`,`amount`) values('%s','%s','%f','%f','%f','%f','%s','%s'); " % (
                row['code'], index, row['open'], row['high'], row['close'], row['low'], row['volume'], row['amount'])
            db1.cursor.execute(sql)
            db1.db.commit()


def setLastUpdateTime():
    sql = "insert into DATA.updatetime(dt) values(%s)" % (datetime.datetime.now())
    db1.cursor.execute(sql)
    db1.db.commit()


def main(duration):
    selectIntoLocal(int(getDuration()))
    setLastUpdateTime()
