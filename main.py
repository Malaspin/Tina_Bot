import telebot
from class_ import User
from openai import OpenAI

API_TOKEN = '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'
token='8065088847:AAEOxYBc1cAl8OmDg3bd-7uvwZKu1fzNzwI'

user = User()

HELP = """
1. /start - покажет приветственное сообщение
2. /add - начнет процесс регистрации нового пользователя
3. /show - покажет данные введеного пользователя
4  /say - начнет диалог после создания пользователя. Может быть пинг.
5. Что бы остановить разговор просто введите stop
"""

bot=telebot.TeleBot(token)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,f'{HELP}')

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, 'Как тебя зовут?')
    bot.register_next_step_handler(message, name_)
def name_(message):
    user.user_name = message.text
    bot.send_message(message.chat.id, 'Какой твой родной язык?')
    bot.register_next_step_handler(message, user_lang)
def user_lang(message):
    user.user_language = message.text
    bot.send_message(message.chat.id, 'Какой язык ты учишь?')
    bot.register_next_step_handler(message, learn_lang)
def learn_lang(message):
    user.learn_language = message.text
    bot.send_message(message.chat.id, 'Насколько хорошо ты владеешь языком, который учишь?')
    bot.register_next_step_handler(message, level_lang)
def level_lang(message):
    user.level_learn_language = message.text
    user.register()
    return user

@bot.message_handler(commands=['show'])
def show_user(message):
    bot.send_message(message.chat.id, user.show())

@bot.message_handler(commands=['say'])
def say_ai(message):
    bot.send_message(message.chat.id, """Вы запустили диалог с AI собеседником. Ни в коем случае не передавайте ему
персональную информацию. Это небезопасно. Помните - все что сказано AI может и будет
использовано для анализа и обучения AI""")

    completion = client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-r1-0528:free",
        messages = [{"role": "user", "content": user.first_messages}]
    )
    response = completion.choices[0].message.content
    user.add_ai_mess(response)
    bot.send_message(message.chat.id, f'{response}')
    bot.register_next_step_handler(message, deepseek_ai)

def deepseek_ai(message): # Работаем с промтом, нужно из класса пользователя подтянуть всякое разное
    if message.text == 'stop':
        user.dialog_log.clear()
        return bot.send_message(message.chat.id, 'Пока')
    else:
        completion = client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-r1-0528:free",
            messages = [{"role": "user", "content": f'Лог диалога {user.dialog_log}. Новое сообщение пользователя: {message.text}. Продолжай диалог.'}]
        )
        user.add_user_mess(message.text)
        response = completion.choices[0].message.content
        user.add_ai_mess(response)
        bot.send_message(message.chat.id, f'{response}')
        bot.register_next_step_handler(message, deepseek_ai)


bot.infinity_polling(timeout=10, long_polling_timeout=5)

