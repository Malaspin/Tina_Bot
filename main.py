import telebot


token='8065088847:AAEOxYBc1cAl8OmDg3bd-7uvwZKu1fzNzwI'

bot=telebot.TeleBot(token)

user_data = [{'admin':[{'user_language':'Russian'},{'level_language':'beginer'}]}]
user_name = {}
user_language = {}
language_level = {}

# username = input('What is your name? ')
#
# def data_add(username):
#     user_language = input('Your native language? ')
#     level_language = input('You language level? ')
#     user_list.append({username:[{'user_native_language':user_language},{'user_level_language':level_language}]})
#
# def user_add(username):
#     for name in user_data:
#         if username in name:
#             print('username used')
#         else:
#             data_add(username)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет ✌️ ")

@bot.message_handler(commands=['add_user'])
def name_(message):
    name = message.text.split(maxsplit=1)[1]
    user_name['name'] = name

@bot.message_handler(commands=['user_language'])
def language_(message):
    user_language = message.text.split(maxsplit=1)[1]
    return user_language

@bot.message_handler(commands=['language_level'])
def level_(message):
    language_level = message.text.split(maxsplit=1)[1]
    return language_level


@bot.message_handler(commands=['show'])
def show_(message):
    bot.send_message(message.chat.id, f'Your {user_name['name']}, native language {user_language}, level language {language_level}')

# def user_add(mesage):
#     for name in user_data:
#         if 'Malaspim' in name:
#             print('username used')
#         else:
#             user_data.append({'Malaspim':[{'user_native_language':'user_language'},{'user_level_language':'level_language'}]})
#             print(user_data)

bot.infinity_polling()
