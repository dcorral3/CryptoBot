import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo

def coinMainKeyboard():
    inline_key = [[InlineKeyboardButton(text='<-Back', callback_data='back')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_key)

def coinMainTxt(coin):
    return coin['name'] + '\n' + coin['value'] + ' USD'

def keyBoardGenerator(columns = 1, cursor = None):
    inline_key = []
    if cursor:
        for i in range(0, cursor.count(), columns):
            raw_buttons = []
            if (cursor.count()-i) < columns:
                columns = cursor.count()-i
            for c in range(0, columns, 1):
                raw_buttons.append(
                            InlineKeyboardButton(
                                text=cursor[i+c]['name'],
                                callback_data=cursor[i+c]['shortName']
                            )
                        )
            inline_key.append(raw_buttons)
        return InlineKeyboardMarkup(inline_keyboard=inline_key)


def coinListView(coinCursor, bot, msg, start=None):
    if start:
        bot.sendMessage(
            msg['chat']['id'],
            'Choose a coin:',
            reply_markup=keyBoardGenerator(2, coinCursor)
            )
    else:
        bot.editMessageText(
                (msg['from']['id'], msg['message']['message_id']),
                'Choose a coin:',
                reply_markup=keyBoardGenerator(2, coinCursor)
                )

def coinMainView(coin, bot, msg):
    keyboard = coinMainKeyboard()
    text = coinMainTxt(coin)
    bot.editMessageText(
            (msg['from']['id'], msg['message']['message_id']),
            text,
            reply_markup=keyboard
            )

def helpView(bot, chat_id):
    bot.sendMessage(chat_id, 'HELP?')
