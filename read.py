import csv
import sys
import os
import glob
import datetime

rootdir = '.'
topCoins = 20

coins = {}

def CAGR(first, last, periods):
    return (last/first)**(1/periods)-1

def processFile(file):
    global coins
    dateStr = file.split("/")[1].split(".")[0]
    isLastFile = ".last." in file

    with open(file, "r") as f:
        reader = csv.DictReader(f)

        i = 1
        currFileCoins = {}
        for row in reader:
            try:
                coinName = row["Name"]
                date = datetime.datetime.strptime(dateStr, "%Y%m%d")
                rank = int(row["#"])
                symbol = row["Symbol"]
                price = 0 if row["Price"] == "?" else float(row["Price"].strip("$").replace(",", ""))
                marketCap = 0 if row["Market Cap"] == "?" else float(row["Market Cap"].strip("$").replace(",", ""))

                
                if i <= topCoins:
                    currFileCoins[symbol] = True

                    coin = coins.get(symbol)
                    if not coin:
                        coin = {}
                        coins[symbol] = coin
                        coin["name"] = coinName
                        coin["firstDate"] = date
                        coin["firstRank"] = rank
                        coin["symbol"] = symbol
                        coin["firstPrice"] = price
                        coin["firstMarketCap"] = marketCap
                        coin["inTopWeeksCount"] = 0
                        coin["enterTopCount"] = 0
                        coin["isTop"] = False

                        coin["lastPrice"] = 0.0
                        coin["lastDate"] = "NA"
                        coin["lastMarketCap"] = 0.0
                        coin["lastRank"] = 9999
                        coin["CAGR"] = -100.0
                        coin["value"] = 1000
                        coin["value2"] = 1000
                        
                    
                    if not coin["isTop"]:
                        coin["enterTopCount"] = coin["enterTopCount"] + 1
                        coin["_buyPrice"] = price

                    coin["inTopWeeksCount"] = coin["inTopWeeksCount"] + 1
                    if not isLastFile:
                        coin["isTop"] = True
                i = i + 1

                coin = coins.get(symbol)
                if coin:
                    coin["_price"] = price

                if isLastFile and coin:
                    #if not coinName in coins:
                    #    continue
                    coin["lastPrice"] = price
                    coin["lastDate"] = date
                    coin["lastMarketCap"] = marketCap
                    coin["lastRank"] = rank
                    years = (coin["lastDate"] - coin["firstDate"]).days / 365.0
                    coin["CAGR"] = 0 if years == 0 else int(10000*CAGR(coin["firstPrice"], coin["lastPrice"], years))/100.0
                    coin["value"] = coin["value"] * coin["lastPrice"] / coin["firstPrice"]
                    coin["value2"] = coin["value2"] * coin["_price"] / coin["_buyPrice"]

            except:
                print row
                raise
    if not isLastFile:
        for sym in coins:
            coin = coins[sym]
            if not sym in currFileCoins:
                if coin["isTop"]:
                    coin["value2"] = coin["value2"] * coin["_price"] / coin["_buyPrice"]
                coin["isTop"] = False


for filename in sorted(glob.iglob('data/*.csv')):
    processFile(filename)

#w = csv.DictWriter(sys.stdout, coins["Bitcoin"].keys())
#w.writeheader()
w = csv.writer(sys.stdout)
first  = True
for sym in coins:
    coin = coins[sym]
    if coin["CAGR"] == -100.0:
        coin["value"] = 0
    del coin["_price"]
    del coin["_buyPrice"]
    if first:
        w.writerow(coin.keys())
        first = False
    w.writerow(coin.values())
#print coins