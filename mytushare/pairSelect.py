from pandas import DataFrame

import db.DBConnection as db1

stockPriceMatrix = []

relations = []
stocks = []


class Relatetion:
    def __init__(self, code1, code2, re):
        self.code1 = code1
        self.code2 = code2
        self.relation = re

    def __str__(self):
        return str("code1=%s|code2=%s|relation=%s" % (self.code1, self.code2, self.relation))


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
        for data1 in data:
            if data1[0] == stockCode:
                dfdata.append(data1[2])
        stocks.append(Stock(stockCode, DataFrame(data=dfdata)))
        print("load stock code ", str(stockCode), " finish")
    print("load history finish")
    getCov()
    sorted(relations, key=lambda r: r.relation)
    writeFile()


def writeFile():
    with open("/root/pythonTrade/result", "a+") as file:
        for r in relations:
            file.writelines(str(r))


def getCov():
    for stock1 in stocks:
        for stock2 in stocks:
            if stock1.code != stock2.code:
                relations.append(Relatetion(code1=stock1.code, code2=stock2.code,
                                            re=stock1.df[0].astype('float64').corr(stock2.df[0].astype('float64'))))


def main():
    loadData()
