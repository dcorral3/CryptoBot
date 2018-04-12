from datetime import datetime
import requests
import conf.db_config as auth
import pymongo
from pymongo import MongoClient
import json

class Model:
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
        except Exception as e:
            print("DB Error: ", str(e))
        finally:
            self.coinList = self.db.coins.find()

    def urlGenerator(self, symbol):
        return "https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+symbol+"&tsyms=USD"

    def getCoinList(self):
        return self.coinList

    def getCoin(self, symbol):
        coinObj = self.db.coins.find_one({'symbol': symbol})
        url = self.urlGenerator(symbol)
        req = requests.get(url)
        data = req.json()
        if req.status_code == 200 and coinObj:
            value = data['RAW'][symbol]['USD']['PRICE']
            update_time=datetime.fromtimestamp(
                    data['RAW'][symbol]['USD']['LASTUPDATE']
                    ).strftime("%H:%M:%S")
            coin = {'name': coinObj['name'],
                    'symbol': symbol,
                    'value': str(value),
                    'time': update_time}
        else:
            coin = None
        return coin
