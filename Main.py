from datetime import datetime, time
import pandas as pd
from binance.client import Client
from pprint import pprint
import os


API_KEY = os.environ["Binance_api_key"]
SEC_KEY = os.environ["Binance_sec_key"]
client = Client(API_KEY, SEC_KEY)

class binanop:
    def __init__(self,earn_wallet):
        self.earn_money = self.Money(earn_wallet)
        self.spot_money = self.Money(self.Spot_wallet())
        self.total_money = self.earn_money + self.spot_money
        print("Money is : {} \n Spot = {} Earn = {} ".format(self.total_money,self.spot_money,self.earn_money))
        
    def Spot_wallet(self):
        wallet = {}
        orders = client.get_account()
        for i in orders["balances"]:
            if float(i["free"]) != float(0) or float(i["locked"]) != float(0):
                wallet[i["asset"]] = float(i["free"]) + float(i["locked"])
        return wallet # return spot balance

    def Get_price(self,currency):
        prices = {}
        endwith = currency
        Data_raw = client.get_all_tickers()
        for i in range(len(Data_raw)):
            if Data_raw[i]["symbol"].endswith(endwith):
                prices[Data_raw[i]["symbol"]] = float(Data_raw[i]["price"])
        return prices # return All pices with current currency

    def Money(self,wallet):
        sum = 0
        currency = "BUSD"
        price = self.Get_price(currency)
        for coin in list(wallet.keys()):
            if coin != currency:
                sum = sum + (float(wallet[coin])*float(price[coin+currency]))
            elif coin == currency:
                sum = sum + float(wallet[coin])
        return sum

earn_wallet = {"EGLD" : "2.28665609"}
mywallet = binanop(earn_wallet)
read = pd.read_csv("Book1.csv").set_index("Date")
read.loc[datetime.now()] = mywallet.total_money
write = pd.ExcelWriter("Book1.csv")
read.to_csv(write,"Book1")