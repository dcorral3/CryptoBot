from model.model import Model
import view.view as view
import telepot
print("loading controller...")
class Controller:
    def __init__(self, bot=None):
        self.bot=bot
        self.model=Model()

    def handler(self, msg):
        flav = telepot.flavor(msg)

        if flav is 'chat':
            self.__chatCmd(msg)
        elif flav is 'callback_query':
            self.__callbackQueryCmd(msg)
            self.bot.answerCallbackQuery(msg['id'])
        else:
            print("Default")



    #control commands in chat

    def __chatCmd(self, msg):

        if '/start' == msg['text']:
            coins = self.model.getCoinList()
            view.coinListView(coins, self.bot, msg, True)
            
        elif '/top10' == msg['text']:
            coins = self.model.getCoinList()
            view.coinListView(coins, self.bot, msg, True)

        elif '/help' in msg['text']:
            view.helpView(self.bot, msg['chat']['id'])

        else: #default
            view.helpView(self.bot, msg['chat']['id'])




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
