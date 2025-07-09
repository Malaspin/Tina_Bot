class User:

    users = {}

    dialog_log = {}

    def __init__(self, user_name = None, user_language = None, learn_language = None, level_learn_language = None):
        self.user_name = user_name
        self.user_language = user_language
        self.learn_language = learn_language
        self.level_learn_language = level_learn_language

    def register(self):
        if self.user_name == None or '/' in User.users:
            return 'Недопустимое имя пользователя'
        elif self.user_name in User.users:
            return 'Логин занят, попробуйте снова'
        else:
            User.users[self.user_name] = {'user_language':self.user_language,
                                          'learn_language': self.learn_language,
                                          'level_learn_language':self.level_learn_language}

    def show(self):
        return f'Вас зовут {self.user_name}, ваш язык {self.user_language}, вы изучаете {self.learn_language}, ваш уровень владения изучаемым языком {self.level_learn_language}'

    @property
    def first_messages(self):
        first_mess = (f"""Ты выполняешь роль собеседника, имя пользователя {self.user_name} 
        язык пользователя {self.user_language},
        пользователь изучает {self.learn_language}, 
        уровень владения изучаемым языком у пользователя {self.level_learn_language}
        общайся с пользователем на {self.learn_language}. 
        Не давай пояснений, комментариев и переводов, пока пользователь не попросит. 
        Используй разговорный язык. Обращайся к пользователю по имени. 
        Симулируй стиль общения живого человека. 
        Используй все стили написания которые используются в изучаемом языке. 
        В ответ начни разговор как человек, задай тему диалога. Никогда не передавай в ответ пустую строку""")
        User.dialog_log['start_mess'] = first_mess
        return first_mess

    def add_ai_mess(self, response):
        User.dialog_log['ai_message'] = f'{response}'

    def add_user_mess(self, message):
        User.dialog_log['user_message'] = f'{message}'

