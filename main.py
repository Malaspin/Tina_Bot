import telebot


token='8065088847:AAEOxYBc1cAl8OmDg3bd-7uvwZKu1fzNzwI'

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет ✌️ ")

bot.infinity_polling()