import requests
import conf.db_config as auth
import pymongo
from pymongo import MongoClient
import json

class model:
    coins = [
              { '_id': 0, 'name': 'Bitcoin', 'symbol': 'BTC'},
              { '_id': 1, 'name': 'Ethereum', 'symbol': 'ETH'},
              { '_id': 2, 'name': 'Ripple', 'symbol': 'XRP'},
              { '_id': 3, 'name': 'BiCash', 'symbol': 'BCH'},
              { '_id': 4, 'name': 'Litecoin', 'symbol': 'LTC'},
              { '_id': 5, 'name': 'EOS', 'symbol': 'EOS'},
              { '_id': 6, 'name': 'Cardano', 'symbol': 'ADA'},
              { '_id': 7, 'name': 'Stellar', 'symbol': 'XLM'},
              { '_id': 8, 'name': 'NEO', 'symbol': 'NEO'},
              { '_id': 9, 'name': 'IOTA', 'symbol': 'IOT'}
          ]

    def __init__(self):
        self.db = MongoClient(
                host = auth.host,
                username = auth.username,
                password = auth.password,
                authSource = auth.authSource
                )[auth.authSource]
        try:
            self.db.coins.insert(self.coins)
        except:
            pass
        finally:
            self.coinList = self.db.coins.find()

    def urlGenerator(self, coinName):
        return "https://min-api.cryptocompare.com/data/price?fsym="+ coinName +"&tsyms=USD,EUR"

    def getCoinList(self):
        return self.coinList

    def getCoin(self, symbol):
        coinObj = self.db.coins.find_one({'symbol': symbol})
        url = self.urlGenerator(symbol)
        req = requests.get(url)
        if req.status_code == 200 and coinObj:
            value = req.json()['USD']
            coin = {'name': coinObj['name'],'value': str(value)}
        else:
            coin = None
        return coin
