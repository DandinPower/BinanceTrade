import matplotlib.pyplot as plt
from binance.client import Client
api_key = ""
api_secret = ""

wallet = {"ETH": 0, "USDT": 16.87}


def buy(price, wallet):
    if(wallet["USDT"] != 0):
        TempETH = wallet["USDT"]/price
        wallet["USDT"] = 0
        wallet["ETH"] = wallet["ETH"] + TempETH
    return wallet


def sell(price, wallet):
    if(wallet["ETH"] != 0):
        TempUSDT = wallet["ETH"] * price
        wallet["ETH"] = 0
        wallet["USDT"] = wallet["USDT"] + TempUSDT
    return wallet


client = Client(api_key, api_secret)
OpenList = []
CloseList = []
HighList = []
LowList = []
RviList = []
SignalList = []
Time = []
i = 0
for kline in client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_5MINUTE,  "22 April, 2021", "23 April, 2021"):
    Open = float(kline[1])
    OpenList.append(Open)
    High = float(kline[2])
    HighList.append(High)
    Low = float(kline[3])
    LowList.append(Low)
    Close = float(kline[4])
    CloseList.append(Close)
    Time.append(i)
    i += 1
for j in range(i):
    if(j >= 3):
        Open = OpenList[j]
        Open_1 = OpenList[j-1]
        Open_2 = OpenList[j-2]
        Open_3 = OpenList[j-3]
        Close = CloseList[j]
        Close_1 = CloseList[j-1]
        Close_2 = CloseList[j-2]
        Close_3 = CloseList[j-3]
        High = HighList[j]
        High_1 = HighList[j-1]
        High_2 = HighList[j-2]
        High_3 = HighList[j-3]
        Low = LowList[j]
        Low_1 = LowList[j-1]
        Low_2 = LowList[j-2]
        Low_3 = LowList[j-3]
        TempMov = ((Close - Open) + (2 * (Close_1-Open_1)) +
                   (2 * (Close_2-Open_2)) + (Close_3 - Open_3))/6
        TempRange = ((High - Low) + (2 * (High_1-Low_1)) +
                     (2 * (High_2-Low_2)) + (High_3 - Low_3))/6
        TempRVI = TempMov/TempRange
        RviList.append(TempRVI)
    else:
        RviList.append(0)
for j in range(i):
    if(j >= 3):
        Rvi = RviList[j]
        Rvi_1 = RviList[j-1]
        Rvi_2 = RviList[j-2]
        Rvi_3 = RviList[j-3]
        TempSignal = (Rvi + (2 * Rvi_1) + (2 * Rvi_2) + Rvi_3)/6
        SignalList.append(TempSignal)
    else:
        SignalList.append(0)
BuyTimeList = []
BuyList = []
SellTimeList = []
SellList = []
buystate = True
sellstate = False
for j in range(1, i-1):
    rvi_next = RviList[j+1]
    rvi = RviList[j]
    rvi_1 = RviList[j-1]
    signal_next = SignalList[j+1]
    signal = SignalList[j]
    signal_1 = SignalList[j-1]
    price = OpenList[j]
    if(rvi_1 < 0):
        if(rvi > signal and buystate):
            if(signal_1 > rvi_1):
                wallet = buy(price, wallet)
                buystate = False
                sellstate = True
                BuyTimeList.append(j)
                BuyList.append(price)
                print(wallet)
    if(signal_1 > 0):
        if(rvi < signal and sellstate):
            if(signal_1 > rvi_1):
                wallet = sell(price, wallet)
                buystate = True
                sellstate = False
                SellTimeList.append(j)
                SellList.append(price)
                print(wallet)
for j in range(i):
    for x in range(len(BuyTimeList)):
        if BuyTimeList[x] == j:
            print("buy", j, BuyList[x])
    for x in range(len(SellTimeList)):
        if SellTimeList[x] == j:
            print("sell", j, SellList[x])

if(sellstate):
    print(wallet["ETH"]*OpenList[-1])

plt.figure(figsize=(15, 10), dpi=100, linewidth=2)
plt.plot(Time, SignalList, 's-', color='r')
plt.plot(Time, RviList, 'o-', color='g')

plt.figure(figsize=(15, 10), dpi=100, linewidth=2)
plt.plot(Time, OpenList, 's-', color='b')
plt.show()
