'''
此版本為測試下單功能
'''
from binance.client import Client
from decimal import Decimal
api_key = ""
api_secret = ""


def Float(money):  # 將過多的小數點去除
    money = str(money)
    money = Decimal(money).quantize(Decimal('0.00000'))
    return float(money)


client = Client(api_key, api_secret)
prices = client.get_all_tickers()  # 取得ETH/USDT價格
for index in prices:
    if(index["symbol"] == "ETHUSDT"):
        price = index["price"]
info = client.get_account()
balances = info["balances"]  # 取得錢包餘額
ETHUSDT = float(price)
ETH = float(balances[2]['free'])
USDT = float(balances[11]['free'])

Quan = Float(USDT/ETHUSDT*0.9995)  # 下買單(時價)
order = client.order_market_buy(
    symbol='ETHUSDT', quantity=Quan)

Quan = Float(ETH * 0.9995)  # 下賣單(時價)
order = client.order_market_sell(
    symbol='ETHUSDT', quantity=Quan)
