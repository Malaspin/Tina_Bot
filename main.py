import json
import time
import os
from dotenv import load_dotenv
from class_ import User
from class_ import DataBase
import telebot
from openai import OpenAI

# From .env we get environment variables
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
token = os.getenv('BOT_TOKEN')

#Create a user object. (When rewriting to async, it will be changed)
user = User()

HELP = """
1. /start - покажет приветственное сообщение и аутентифицирует пользователя, если он ранее обращался к боту
2. /add - начнет процесс регистрации нового пользователя
3. /show - покажет данные введеного пользователя
4  /say - начнет диалог после создания пользователя. Может быть пинг.
5. Что бы остановить разговор просто введите stop
"""

#We raise the database. We unload data from it into RAM
user_db = DataBase('.user_log', 'users')
user_db.db_crate('users')
User.users = {}
try:
    data_base_user = user_db.db_reade('users')
    for data_user in data_base_user:
        user.users[data_user[1]] = {
            'user_name': data_user[2],
            'user_language': data_user[3],
            'learn_language': data_user[4],
            'level_learn_language': data_user[5]}
except:
    pass

#Initiate the bot
bot=telebot.TeleBot(token)

#Initiating the OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_TOKEN,)

#Starting message. User authentication is built in here
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id,f'{HELP}')
    user.user_authentication(message.json['from']['id'])

#Registration process. Also built-in authentication to avoid duplication of users
@bot.message_handler(commands=['add'])
def add(message):
    user.user_id = message.json['from']['id']
    user.user_authentication(user.user_id)
    if user.user_id in User.users:
        bot.send_message(message.chat.id, f'Добро пожаловать {user.user_name}')
    else:
        bot.send_message(message.chat.id, 'Как тебя зовут?')
        bot.register_next_step_handler(message, name_)
def name_(message):
    user.user_name = message.text.lower()
    bot.send_message(message.chat.id, 'Какой твой родной язык?')
    bot.register_next_step_handler(message, user_lang)
def user_lang(message):
    user.user_language = message.text.lower()
    bot.send_message(message.chat.id, 'Какой язык ты учишь?')
    bot.register_next_step_handler(message, learn_lang)
def learn_lang(message):
    user.learn_language = message.text.lower()
    bot.send_message(message.chat.id, 'Насколько хорошо ты владеешь языком, который учишь?')
    bot.register_next_step_handler(message, level_lang)
def level_lang(message):
    user.level_learn_language = message.text.lower()
    if user.user_id not in User.users:
        user_db.db_insert('users',
                          user.user_id,
                          user.user_name,
                          user.user_language,
                          user.learn_language,
                          user.level_learn_language,
                          f'.user_log/{user.user_id}_messages_log.json')
        user.register()
        bot.send_message(message.chat.id, 'Вы успешно зарегистрированы. Для начала диалога с нажмите /say')
        return user

#The service part allows the user to view their data
@bot.message_handler(commands=['show'])
def show_user(message):
    bot.send_message(message.chat.id, user.show())

#Starting a dialogue with a neural network
@bot.message_handler(commands=['say'])
def say_ai(message):
    bot.send_message(message.chat.id, """Вы запустили диалог с AI собеседником. Ни в коем случае не передавайте ему
персональную информацию. Это небезопасно. Помните - все что сказано AI может и будет
использовано для анализа и обучения AI""")
    #Reading message logs from previous sessions into memory
    try:
        id_ = message.json['from']['id']
        with open(f'{user_db.db_reade('users', id_, 'file_log')[0][0]}', 'r', encoding='utf-8') as log:
            data_log = json.load(log)
            usr_log = data_log
            user.dialog_log = usr_log[-5:]
    except FileNotFoundError:
        pass
    #Sending the starting prompt
    completion = client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-r1-0528:free",
        messages = [{"role": "user", "content": f'Start message {user.first_messages}'}])
    response = completion.choices[0].message.content
    user.add_mess_log(message.text, response)
    bot.send_message(message.chat.id, f'{response}')
    bot.register_next_step_handler(message, deepseek_ai)

#Cyclic work with neural network
def deepseek_ai(message):
    if message.text.lower() == 'stop' or message.text.lower() == 'стоп':
        user.log_json_write()
        user.dialog_log.clear()
        return bot.send_message(message.chat.id, 'Пока')
    else:
        time_start = time.time()
        completion = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-r1-0528:free",
            messages = [
                {"role": "user",
                 "content": f'\
                 Start message {user.first_messages}\
                 Chat log {user.dialog_log[-5:]}\
                 New message from user: {message.text}. \
                 Continue the dialogue - answer with a string, not json.'}
            ]
        )
        time_end = time.time()
        work_time = time_end-time_start
        print(f'Work time: {work_time:.6f}')
        response = completion.choices[0].message.content
        user.add_mess_log(message.text, response)
        if response:
            bot.send_message(message.chat.id, f'{response}')
        else:
            bot.send_message(message.chat.id, f'Нейронка затупила, пустой ответ. Попробуй еще раз, либо перезапусти чат "/say"' )
        bot.register_next_step_handler(message, deepseek_ai)

bot.infinity_polling(timeout=10, long_polling_timeout=5)