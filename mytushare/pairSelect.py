import pandas as pd
from pandas import DataFrame

import db.DBConnection as db1

stockPriceMatrix = []

stocks = []

map = {}

validDuration = 50


class Relatetion:
    def __init__(self, code1, code2, re):
        self.code1 = code1
        self.code2 = code2
        self.relation = re

    def __str__(self):
        return str("code1=%s|code2=%s|relation=%s" % (self.code1, self.code2, self.relation))

    def save(self):
        sql = "insert into DATA.relation(`code1`,`code2`,`relation`) values('%s','%s','%s'); " % (
            self.code1, self.code2, self.relation)
        db1.cursor.execute(sql)
        db1.db.commit()


class Stock:
    def __init__(self, code, df):
        self.code = code
        self.df = df


def loadData():
    sql = """SELECT
  t12.`code`,
  t12.`date`,
  t12.`close`
FROM (SELECT *
      FROM h_data AS t1
      GROUP BY t1.code, t1.close) AS t12
ORDER BY t12.code, t12.date;"""
    cursor = db1.cursor
    cursor.execute(sql)
    data = cursor.fetchall()
    stocksset = set([])
    # 获取所有Code
    for data1 in data:
        stocksset.add(data1[0])
    print("load stock code finish")
    # 建立树形结构
    for stockCode in stocksset:
        dfdata = []
        Index1 = []
        for data1 in data:
            if data1[0] == stockCode:
                Index1.append(data1[1])
                dfdata.append(data1[2])
        stocks.append(Stock(stockCode, DataFrame(index=Index1,
                                                 columns=["close"], data=dfdata)))
        print("load stock code ", str(stockCode), " finish")
    print("load history finish")
    getCov()
    print("cal Finish")


def getCov():
    for stock1 in stocks:
        for stock2 in stocks:
            if stock1.code != stock2.code:
                if map.get(str(stock1.code) + str(stock2.code)) == 1 or map.get(
                        str(stock2.code) + str(stock1.code)) == 1:
                    continue
                else:
                    dfArr = getSomeDurationData(stock1, stock2)
                    if dfArr.size >= validDuration:
                        re = dfArr['close_x'].astype('float64').corr(dfArr['close_y'].astype('float64'))
                        Relatetion(code1=stock1.code, code2=stock2.code,
                                   re=re).save()
                        map[str(stock1.code) + str(stock2.code)] = 1


def getSomeDurationData(df1, df2):
    longDf = df1.df
    shortDf = df2.df
    return pd.merge(shortDf, longDf, left_index=True, right_index=True)


def main():
    loadData()


main()
