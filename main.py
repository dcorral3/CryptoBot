import telepot
import bot_config

bot = telepot.Bot(bot_config.token)
print(bot.getMe())


