import bot_config
import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot(bot_config.token)
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
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
    keyArr = [keyboard,keyboard]
    bot.sendMessage(chat_id, 'Chose a coin:', reply_markup=keyboard)


MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)
