from model.model import Model
from .commandHandler import CommandHandler
import view.view as view
import telepot
from telepot.routing import (lower_key, by_chat_command, make_routing_table)

print("loading controller...")
class Controller:

    def __init__(self, bot=None):
        self.bot=bot
        self.model=Model()

        command_handler = CommandHandler(self.bot, self.model)
        self.command_router = telepot.helper.Router(lower_key(by_chat_command()),
                                           make_routing_table(command_handler, [
                                               'start',
                                               'top10',
                                               'help',
                                               (None, command_handler.on_invalid_command),
                                           ]))

        self.bot._router.routing_table['chat'] = self.command_router.route

    def handler(self, msg):
        flav = telepot.flavor(msg)

        if flav is 'chat':
            self.command_router.route(msg)
        elif flav is 'callback_query':
            self.__callbackQueryCmd(msg)
            self.bot.answerCallbackQuery(msg['id'])
        else:
            print("Default")


    #control callbacks

    def __callbackQueryCmd(self, msg):

        data = msg['data']

        if 'back' in data:
            coins = self.model.getCoinList()
            view.coinListView(coins, self.bot, msg)

        elif 'coin' in data: #coin button callback
            coinData = data.split()
            coin = self.model.getCoin(coinData[1])
            view.coinMainView(coin, self.bot, msg)
