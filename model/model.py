import requests
import conf.db_config as auth
import pymongo
from pymongo import MongoClient
import json

class model:
    coins = [
              { '_id': 0, 'name': 'Bitcoin', 'shortName': 'BTC'},
              { '_id': 1, 'name': 'Ethereum', 'shortName': 'ETH'},
              { '_id': 2, 'name': 'Ripple', 'shortName': 'XRP'},
              { '_id': 3, 'name': 'BiCash', 'shortName': 'BCH'},
              { '_id': 4, 'name': 'Litecoin', 'shortName': 'LTC'},
              { '_id': 5, 'name': 'EOS', 'shortName': 'EOS'},
              { '_id': 6, 'name': 'Cardano', 'shortName': 'ADA'},
              { '_id': 7, 'name': 'Stellar', 'shortName': 'XLM'},
              { '_id': 8, 'name': 'NEO', 'shortName': 'NEO'},
              { '_id': 9, 'name': 'IOTA', 'shortName': 'IOT'}
          ]

    def __init__(self):
        self.db = MongoClient(
                host = auth.host,
                username = auth.username,
                password = auth.password,
                authSource = auth.authSource
                )[auth.authSource]
        self.coinList = self.db.coins.find()
        try:
            self.db.coins.insert(self.coins)
        except:
            pass

    def urlGenerator(self, coinName):
        return "https://min-api.cryptocompare.com/data/price?fsym="+ coinName +"&tsyms=USD,EUR"

    def getCoinList(self):
        return self.coinList

    def getCoin(self, coinName):
        coinObj = self.db.coins.find_one({'shortName': coinName})
        url = self.urlGenerator(coinName)
        req = requests.get(url)
        if req.status_code == 200 and coinObj:
            value = req.json()['USD']
            coin = {'name': coinObj['name'],'value': str(value)}
        else:
            coin = None
        return coin
