import tushare as ts

stockPriceMatrix = []
relatetions = []


class Relatetion:
    def __init__(self, code1, code2, re):
        self.code1 = code1
        self.code2 = code2
        self.relation = re


# 如果近duration的均值偏离值小于offsetrate且近duration2均值偏离值大于offsetrate2则入选
def selectIntoLocal(duration, offsetrate, duration2, offsetrate2):
    stocks = ts.get_stock_basics()
    for stockCode, row in stocks.iterrows():
        df = ts.get_h_data(code=stockCode, start='2017-11-01', end='2018-01-01')
        df.insert(0, 'code', stockCode)
        stockPriceMatrix.append(df)
    getCov()


def getCov():
    # with open("/root/pythonTrade/result", "a+") as file:
    for stock1 in stockPriceMatrix:
        for stock2 in stockPriceMatrix:
            if stock1['code'] == stock2['code']:
                continue
            else:
                relatetions.append(
                    Relatetion(stock1['code'][0], stock2['code'][0], stock1['close'].corr(stock2['close'])))
    print(relatetions)


def main(duration, offsetrate, duration2, offsetrate2):
    selectIntoLocal(int(duration), float(offsetrate), int(duration2), float(offsetrate2))
