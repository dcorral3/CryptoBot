import bot_config
import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot(bot_config.token)


def intiKeyboard(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard = [
                    [
                        InlineKeyboardButton(text='Bitcoin', callback_data='btc'),
                        InlineKeyboardButton(text='Ethereum', callback_data='eth'),
                        InlineKeyboardButton(text='Ripple', callback_data='rpx')
                    ],
                    [
                        InlineKeyboardButton(text='Stellar', callback_data='mlx'),
                        InlineKeyboardButton(text='Bitcoin', callback_data='btc'),
                        InlineKeyboardButton(text='Bitcoin', callback_data='btc')
                    ]
                ]
    )
    bot.sendMessage(chat_id, 'Chose a coin:', reply_markup=keyboard)


def printCoinsKeyboard(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)

    keyboard = InlineKeyboardMarkup(inline_keyboard = [
                    [
                        InlineKeyboardButton(text='Bitcoin', callback_data='btc'),
                        InlineKeyboardButton(text='Ethereum', callback_data='eth'),
                        InlineKeyboardButton(text='Ripple', callback_data='rpx')
                    ],
                    [
                        InlineKeyboardButton(text='Stellar', callback_data='mlx'),
                        InlineKeyboardButton(text='Bitcoin', callback_data='btc'),
                        InlineKeyboardButton(text='Bitcoin', callback_data='btc')
                    ]
                ]
    )

    bot.editMessageText((msg['from']['id'], msg['message']['message_id']), 'Chose a coin:', reply_markup=keyboard)



def printCryptoValue(msg):
    print('Getting crypto info...')
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='<- Back', callback_data='back')],])

    bot.editMessageText((msg['from']['id'], msg['message']['message_id']), 'VALOR', reply_markup=keyboard)






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
