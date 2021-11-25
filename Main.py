import pandas as pd
import time
import datetime
from binance.client import Client
from pprint import pprint
import os


API_KEY = os.environ["Binance_api_key"]
SEC_KEY = os.environ["Binance_sec_key"]
client = Client(API_KEY, SEC_KEY)

def Spot_wallet():
    wallet = {}
    orders = client.get_account()
    for i in orders["balances"]:
        if float(i["free"]) != float(0):
            wallet[i["asset"]] = i["free"]
    return wallet # return spot balance

def Get_price(currency):
    prices = {}
    endwith = currency
    Data_raw = client.get_all_tickers()
    for i in range(len(Data_raw)):
        if Data_raw[i]["symbol"].endswith(endwith):
            prices[Data_raw[i]["symbol"]] = Data_raw[i]["price"]
    return prices # return All pices with current currency

def Money(wallet):
    sum = 0
    currency = "BUSD"
    price = Get_price(currency)
    for coin in list(wallet.keys()):
        if coin != currency:
            sum = sum + (float(wallet[coin])*float(price[coin+currency]))
        elif coin == currency:
            sum = sum + float(wallet[coin])
    return sum

earn_wallet = {"EGLD" : "2.28665609"}
total_money = Money(Spot_wallet()) + Money(earn_wallet)
with open("Today.txt","a+") as money:
    string = "{"+str(datetime.datetime.now())+"} : {" + str(total_money) + "},"
    money.writelines(string)