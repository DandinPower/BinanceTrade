import matplotlib.pyplot as plt
from binance.client import Client
api_key = ""
api_secret = ""
client = Client(api_key, api_secret)
wallet = {"ETH": 0, "USDT": 20}


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


def abs(number):
    if number < 0:
        return -number
    else:
        return number


'''
讀取K線
'''
OpenList = []
CloseList = []
HighList = []
LowList = []
Time = []
Num = 0

for kline in client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_3MINUTE,  "1 day ago UTC"):
    Open = float(kline[1])
    OpenList.append(Open)
    High = float(kline[2])
    HighList.append(High)
    Low = float(kline[3])
    LowList.append(Low)
    Close = float(kline[4])
    CloseList.append(Close)
    Time.append(Num)
    Num += 1
'''
計算rsi
'''
rsi_k = 6
RsiList = []
for j in range(Num):
    if (j >= rsi_k):
        TempUp = 0
        TempDown = 0
        for i in range(rsi_k):
            TempValue = CloseList[j-i] - OpenList[j-i]
            if TempValue >= 0:
                TempUp += TempValue
            else:
                TempDown += TempValue
        TempUp = TempUp/rsi_k
        TempDown = abs(TempDown/rsi_k)
        TempRsi = TempUp/(TempDown+TempUp)
        RsiList.append(TempRsi)
    else:
        RsiList.append(0)
'''
計算Rvi
'''
RviList = []
SignalList = []
for j in range(Num):
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
for j in range(Num):
    if(j >= 3):
        Rvi = RviList[j]
        Rvi_1 = RviList[j-1]
        Rvi_2 = RviList[j-2]
        Rvi_3 = RviList[j-3]
        TempSignal = (Rvi + (2 * Rvi_1) + (2 * Rvi_2) + Rvi_3)/6
        SignalList.append(TempSignal)
    else:
        SignalList.append(0)

'''
模擬購買
'''
BuyTimeList = []
BuyList = []
SellTimeList = []
SellList = []
buystate = True
sellstate = False
for j in range(1, Num-1):
    rvi_next = RviList[j+1]
    rvi = RviList[j]
    rvi_1 = RviList[j-1]
    signal_next = SignalList[j+1]
    signal = SignalList[j]
    signal_1 = SignalList[j-1]
    price = OpenList[j]
    rsi = RsiList[j]
    if(rsi > 0.5):
        if(rvi_1 < -0.15):
            if(rvi > signal and buystate):
                if(signal_1 > rvi_1):
                    wallet = buy(price, wallet)
                    buystate = False
                    sellstate = True
                    BuyTimeList.append(j)
                    BuyList.append(price)
                    print(wallet)
        if(signal_1 > 0.15):
            if(rvi < signal and sellstate):
                if(signal_1 > rvi_1):
                    wallet = sell(price, wallet)
                    buystate = True
                    sellstate = False
                    SellTimeList.append(j)
                    SellList.append(price)
                    print(wallet)
for j in range(Num):
    for x in range(len(BuyTimeList)):
        if BuyTimeList[x] == j:
            print("buy", j, BuyList[x], RsiList[j])
    for x in range(len(SellTimeList)):
        if SellTimeList[x] == j:
            print("sell", j, SellList[x], RsiList[j])

if(sellstate):
    print(wallet["ETH"]*OpenList[-1])


'''
印出圖表
'''

plt.figure(figsize=(15, 10), dpi=100, linewidth=2)
plt.plot(Time, SignalList, 's-', color='r')
plt.plot(Time, RviList, 'o-', color='g')

'''
plt.figure(figsize=(15, 10), dpi=100, linewidth=2)
plt.plot(Time, RsiList, 's-', color='r')'''

plt.figure(figsize=(15, 10), dpi=100, linewidth=2)
plt.plot(Time, OpenList, 's-', color='b')
plt.plot(BuyTimeList, BuyList, '^', color='g')
plt.plot(SellTimeList, SellList, '^', color='r')
plt.show()
