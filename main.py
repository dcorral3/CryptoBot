import conf.bot_config as bot_config
from controller.controller import Controller
import time
import telepot
from telepot.loop import MessageLoop

bot = telepot.Bot(bot_config.token)
c = Controller(bot)

MessageLoop(bot, c.handler).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)
