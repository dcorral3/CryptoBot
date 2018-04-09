import conf.bot_config as bot_config
from controller.controller import Controller
import time
import requests
import json
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

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
    bot.sendMessage(chat_id, 'Choose a coin:', reply_markup=keyboard)

def printCoinsKeyboard(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)
    keyboard = getCointKeyboard()
    bot.editMessageText((msg['from']['id'], msg['message']['message_id']),'Choose a coin:', reply_markup=keyboard)
    bot.answerCallbackQuery(query_id)


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
        bot.answerCallbackQuery(query_id)
    else:
        bot.answerCallbackQuery(query_id, text='An error ocurred. Please, try again later.')

bot = telepot.Bot(bot_config.token)
c = Controller(bot)

MessageLoop(bot,c.handler).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)
