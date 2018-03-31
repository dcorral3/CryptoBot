import bot_config
import sys
import time
import telepot
import requests
import json
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot(bot_config.token)


def intiKeyboard(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard = [
                    [
                        InlineKeyboardButton(text='Bitcoin', callback_data='BTC'),
                        InlineKeyboardButton(text='Ethereum', callback_data='ETH'),
                        InlineKeyboardButton(text='Ripple', callback_data='RPX')
                    ],
                    [
                        InlineKeyboardButton(text='Stellar', callback_data='MLX'),
                        InlineKeyboardButton(text='Bitcoin', callback_data='BTC'),
                        InlineKeyboardButton(text='Bitcoin', callback_data='BTC')
                    ]
                ]
    )
    bot.sendMessage(chat_id, 'Chose a coin:', reply_markup=keyboard)


def printCoinsKeyboard(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)

    keyboard = InlineKeyboardMarkup(inline_keyboard = [
                    [
                        InlineKeyboardButton(text='Bitcoin', callback_data='BTC'),
                        InlineKeyboardButton(text='Ethereum', callback_data='ETH'),
                        InlineKeyboardButton(text='Ripple', callback_data='RPX')
                    ],
                    [
                        InlineKeyboardButton(text='Stellar', callback_data='MLX'),
                        InlineKeyboardButton(text='Bitcoin', callback_data='BTC'),
                        InlineKeyboardButton(text='Bitcoin', callback_data='BTC')
                    ]
                ]
    )

    bot.editMessageText((msg['from']['id'], msg['message']['message_id']), 'Chose a coin:', reply_markup=keyboard)



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






MessageLoop(bot, {'chat': handle,
				'callback_query': on_callback_query}).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)
