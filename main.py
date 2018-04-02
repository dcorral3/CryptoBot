import bot_config
import db_config as auth
import time
import telepot
import requests
import json
import pymongo
from pymongo import MongoClient
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot(bot_config.token)
client = MongoClient(
                        host = auth.host,
                        username = auth.username,
                        password = auth.password,
                        authSource = auth.authSource,
                    )

db = client[auth.authSource]

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
            { '_id': 9, 'name': 'IOTA', 'shortName': 'MIOTA'}
        ]
try:
    db.coins.insert(coins)
except:
    pass

def getCointKeyboard():
    inline_key = []
    coinsCollection = db.coins.find()
    for i in range(0, coinsCollection.count(), 2):
        inline_key.append([
            InlineKeyboardButton(text=str(i+1)+'. '+coinsCollection[i]['name'],callback_data=coinsCollection[i]['shortName']),
            InlineKeyboardButton(text=str(i+2)+'. '+coinsCollection[i+1]['name'],callback_data=coinsCollection[i+1]['shortName'])
            ])
    return InlineKeyboardMarkup(inline_keyboard=inline_key)

def intiKeyboard(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    keyboard = getCointKeyboard()
    bot.sendMessage(chat_id, 'Chose a coin:', reply_markup=keyboard)

def printCoinsKeyboard(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)
    keyboard = getCointKeyboard()
    bot.editMessageText((msg['from']['id'], msg['message']['message_id']), 'Chose a coin:', reply_markup=keyboard)
    bot.answerCallbackQuery(query_id, text="")


def printCryptoValue(msg):
    print('Getting crypto info...')
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)

    data = requests.get('https://min-api.cryptocompare.com/data/price?fsym=' + query_data + '&tsyms=USD,EUR')

    if data.status_code == 200:
        data = data.json()
        print(data)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='<- Back', callback_data='back')],])

        text = '*' + str(data['USD']) + '*' + ' USD' + '\n' +  '*' + str(data['EUR']) + '*' + ' EUR'

        bot.editMessageText((msg['from']['id'], msg['message']['message_id']), text, reply_markup=keyboard, parse_mode='Markdown')
        bot.answerCallbackQuery(query_id, text="")
    else:
        bot.answerCallbackQuery(query_id, text='An error ocurred. Please, try again later.')






def handle(msg):
    intiKeyboard(msg)




def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == 'back':
        printCoinsKeyboard(msg)
    else:
        printCryptoValue(msg)






MessageLoop(bot,{
                    'chat': handle,
                    'callback_query': on_callback_query
                }).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)
