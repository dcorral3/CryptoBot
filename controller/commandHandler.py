from model.model import Model
import view.view as view
import telepot

class CommandHandler(object):

    def __init__(self, bot=None, model=None):
        self.bot = bot
        self.model = model

    def on_start(self, msg):
        coins = self.model.getCoinList()
        view.coinListView(coins, self.bot, msg, True)

    def on_top10(self, msg):
        coins = self.model.getCoinList()
        view.coinListView(coins, self.bot, msg, True)

    def on_help(self, msg):
        view.helpView(self.bot, msg['chat']['id'])

    def on_invalid_command(self, msg):
        view.helpView(self.bot, msg['chat']['id'])
