from pandas import DataFrame

import db.DBConnection as db1

stockPriceMatrix = []


class Relatetion:
    def __init__(self, code1, code2, re):
        self.code1 = code1
        self.code2 = code2
        self.relation = re

    def __str__(self):
        return str("code1=%s|code2=%s|relation=%s" % (self.code1, self.code2, self.relation))


def loadData():
    sql = "select `code`, `date`, `open`, `high`, `close`, `low`, `volume`, `amount` from `DATA`.`h_data`"
    cursor = db1.cursor
    cursor.execute(sql)
    data = cursor.fetchall()
    Index = []
    dfData = []
    columns = ['code', 'open', 'high', 'close', 'low', 'volume', 'amount']
    for data1 in data:
        Index.append(data1[1])
        dfData.append(
            [data1[0], float(data1[2]), float(data1[3]), float(data1[4]), float(data1[5]),
             data1[6], data1[7]])
    stockPriceMatrix.append(DataFrame(data=dfData, index=Index, columns=columns))
    getCov()


def getCov():
    with open("/root/pythonTrade/result", "a+") as file:
        for stock1 in stockPriceMatrix:
            for stock2 in stockPriceMatrix:
                if stock1['code'] == stock2['code']:
                    continue
                else:
                    file.writelines(
                        Relatetion(stock1['code'][0], stock2['code'][0], stock1['close'].corr(stock2['close'])))


def main():
    loadData()
