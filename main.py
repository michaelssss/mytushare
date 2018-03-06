import sys

from mytushare import allStockAvgPrice, pairSelect, dataColletion

if __name__ == "__main__":
    action = sys.argv[5]
    if action == "allst":
        allStockAvgPrice.main(sys.argv[1])
    elif action == "collet":
        dataColletion.main(sys.argv[1])
