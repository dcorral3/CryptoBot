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

    def __chatCmd(self, msg):
        if 'start' in msg['text']:
            coins = self.model.getCoinList()
            view.coinListView(coins, self.bot, msg, True)
        else:
            view.helpView(self.bot, msg['chat']['id'])

    def __callbackQueryCmd(self, msg):
        data = msg['data']
        if 'back' in data:
            coins = self.model.getCoinList()
            view.coinListView(coins, self.bot, msg)
        else:
            coin = self.model.getCoin(data)
            view.coinMainView(coin, self.bot, msg)
