import sys

from mytushare import allStockAvgPrice, pairSelect

if __name__ == "__main__":
    action = sys.argv[5]
    if action == "allst":
        allStockAvgPrice.main(sys.argv[1])
    elif action == "select":
        pairSelect.main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
