import pandas as pd
import time
import datetime
from binance.client import Client
from pprint import pprint
import os
import csv


API_KEY = os.environ["Binance_api_key"]
SEC_KEY = os.environ["Binance_sec_key"]
client = Client(API_KEY, SEC_KEY)
wallet = {}

def Get_wallet():
    orders = client.get_account()
    for i in orders["balances"]:
        if float(i["free"]) != float(0):
            wallet[i["asset"]] = i["free"]
    return wallet

def Get_price(currency):
    prices = {}
    endwith = currency
    Data_raw = client.get_all_tickers()
    for i in range(len(Data_raw)):
        if Data_raw[i]["symbol"].endswith(endwith):
            prices[Data_raw[i]["symbol"]] = Data_raw[i]["price"]
    return prices

def Sum_money():
    sum = 0
    currency = "BUSD"
    wallet = Get_wallet()
    price = Get_price(currency)
    for coin in list(wallet.keys()):
        if coin != currency:
            sum = sum + (float(wallet[coin])*float(price[coin+currency]))
        elif coin == currency:
            sum = sum + float(wallet[coin])
    return sum

print(Sum_money())
