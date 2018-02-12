import db.DBConnection as db


class StockData:
    def __init__(self, code, date, open1, high, close, low, volume, amount):
        self.code = code
        self.date = date
        self.open = open1
        self.high = high
        self.close = close
        self.low = low
        self.volume = volume
        self.amount = amount

    def save(self):
        sql = "insert into DATA.h_data(`code`,`date`,`open`,`high`,`close`,`low`,`volume`,`amount`) values('%s','%s','%f','%f','%f','%f','%s','%s'); " % (
            self.code, self.date, self.open, self.high, self.close, self.low, self.volume, self.amount)
        db.cursor.execute(sql)
        db.db.commit()


def loadAllStock():
    stockmap = {}
    sql = """SELECT
  t12.`code`,
  t12.`date`,
  t12.`open`,
  t12.`high`,
  t12.`close`,
  t12.`low`,
  t12.`volume`,
  t12.`amount`
FROM (SELECT *
      FROM h_data AS t1
      GROUP BY t1.code, t1.close) AS t12
ORDER BY t12.code, t12.date;"""
    cursor = db.cursor
    cursor.execute(sql)
    data = cursor.fetchall()
    for data1 in data:
        stockmap[data1[0]] = []
    for stockCode in stockmap.keys():
        data2 = []
        for data1 in data:
            if data1[0] == stockCode:
                data2.append(StockData(data1[0], data1[1], data1[2], data1[3], data1[4], data1[5], data1[6], data1[7]))
    print("load stock code finish")
    return stockmap
