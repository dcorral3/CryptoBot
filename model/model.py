from datetime import datetime
import requests
import conf.db_config as auth
import pymongo
from pymongo import MongoClient
import json

class Model:

    coins = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=10").json()

    def __init__(self):

        self.coins = self.cleanJson()

        self.db = MongoClient(
                host = auth.host,
                username = auth.username,
                password = auth.password,
                authSource = auth.authSource
                )[auth.authSource]
        try:
            self.db.coins.insert(self.coins)
        except Exception as e:
            print("DB Error: ", str(e))
        finally:
            self.coinList = self.db.coins.find()

    def cleanJson(self):
        coinList = []

        for coin in self.coins:
            my_dict = {}
            my_dict['_id'] = coin['id']
            my_dict['name'] = coin['name']
            my_dict['symbol'] = coin['symbol']
            coinList.append(my_dict)

        return coinList


    def urlGenerator(self, symbol):
        if symbol == 'MIOTA':
            symbol = 'IOT'
        return "https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+symbol+"&tsyms=USD", symbol

    def getCoinList(self):
        return self.coinList

    def getCoin(self, symbol):
        coinObj = self.db.coins.find_one({'symbol': symbol})
        url, symbol = self.urlGenerator(symbol)
        req = requests.get(url)
        data = req.json()
        if req.status_code == 200 and coinObj:
            value = data['RAW'][symbol]['USD']['PRICE']
            update_time = datetime.fromtimestamp(
                    data['RAW'][symbol]['USD']['LASTUPDATE']
                    ).strftime("%H:%M:%S")
            coin = {'name': coinObj['name'],
                    'symbol': symbol,
                    'value': str(value),
                    'time': update_time}
        else:
            coin = None
        return coin
