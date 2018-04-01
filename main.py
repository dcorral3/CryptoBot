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
            { 'name': 'Bitcoin', 'shortName': 'BTC'},
            { 'name': 'Ethereum', 'shortName': 'ETH'},
            { 'name': 'Ripple', 'shortName': 'XRP'},
            { 'name': 'BiCash', 'shortName': 'BCH'},
            { 'name': 'Litecoin', 'shortName': 'LTC'},
            { 'name': 'EOS', 'shortName': 'EOS'},
            { 'name': 'Cardano', 'shortName': 'ADA'},
            { 'name': 'Stellar', 'shortName': 'XLM'},
            { 'name': 'NEO', 'shortName': 'NEO'},
            { 'name': 'IOTA', 'shortName': 'MIOTA'}
        ]

db.coins.insert_many(coins)

def getCointKeyboard():
    inline_key = []
    coinsCollection = db.coins.find()
    for coin in coinsCollection:
        inline_key.append([InlineKeyboardButton(text=coin['name'],callback_data=coin['shortName'])])
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
