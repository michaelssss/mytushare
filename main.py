import sys

from mytushare import allStockAvgPrice, selectTrade

if __name__ == "__main__":
    action = sys.argv[5]
    if action == "allst":
        allStockAvgPrice.main()
    elif action == "select":
        selectTrade.main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
