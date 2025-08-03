import json
import sqlite3


class User:

    users = {}

    def __init__(self, user_id = None, user_name = None, user_language = None, learn_language = None, level_learn_language = None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_language = user_language
        self.learn_language = learn_language
        self.level_learn_language = level_learn_language
        self.dialog_log = []

    def register(self):
        if self.user_name == None:
            return 'Недопустимое имя пользователя'
        elif self.user_name in User.users or self.user_id in User.users:
            return 'Логин занят, попробуйте снова'
        else:
            User.users[self.user_id] = {'user_name': self.user_name,
                                          'user_language': self.user_language,
                                          'learn_language': self.learn_language,
                                          'level_learn_language':self.level_learn_language}

    def show(self):
        return f'Вас зовут {self.user_name}, ваш язык {self.user_language}, вы изучаете {self.learn_language}, ваш уровень владения изучаемым языком {self.level_learn_language}'

    def user_authentication(self, user_id):
        if user_id in User.users:
            self.user_id = user_id
            self.user_name = User.users[user_id]['user_name']
            self.user_language = User.users[user_id]['user_language']
            self.learn_language = User.users[user_id]['learn_language']
            self.level_learn_language = User.users[user_id]['level_learn_language']

    @property
    def first_messages(self):
        first_mess = (f"""Username {self.user_name}.
        User language {self.user_language}.
        User learns language {self.learn_language}.
        The user's level of proficiency in the language being studied {self.level_learn_language}.
        You are a native speaker of {self.learn_language}.
        Communicate with the user only in {self.learn_language}, until you are explicitly asked otherwise.
        Use natural, conversational language appropriate to native speakers.
        Use all the writing styles that are used in the language you are learning.
        In response, start a conversation like a human being.
        Do not make any comments unless you are explicitly asked to.
        Don't translate your messages into the user's language unless you are explicitly asked to do so.
        The answer should not contain any notes, clarifications or other information that is not present in normal human dialogue.  
""")
        return first_mess

    def add_mess_log(self, message, response):
        medium_dict = {}
        medium_dict['user_message'] = message
        medium_dict['ai_message'] = response
        self.dialog_log.append(medium_dict)

    def log_json_write(self):
        try:
            with open(f'.user_log/{self.user_id}_messages_log.json', 'r', encoding='utf-8') as log:
                data = json.load(log)
                data.extend(self.dialog_log)
        except FileNotFoundError:
            data = self.dialog_log.copy()
        self.dialog_log.clear()
        with open(f'.user_log/{self.user_id}_messages_log.json', 'w', encoding='utf-8') as log:
            json.dump(data, log, ensure_ascii=False, indent=2)

class DataBase:

    def __init__(self, address_db, base_name):
        self.base_name = f'{base_name}.db'
        self.address_db = address_db

    def db_crate(self, table_name):
        conn = sqlite3.connect(f'{self.address_db}/{self.base_name}')
        cursor = conn.cursor()
        with conn:
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} 
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_name INTEGER,
            user_name TEXT,
            user_language TEXT,
            learn_language TEXT,
            level_learn_language TEXT,
            file_log TEXT
            )
            """)
        cursor.close()
        conn.close()

    def db_reade(self, table_name, id_name=None, column='*'):
        conn = sqlite3.connect(f'{self.address_db}/{self.base_name}')
        cursor = conn.cursor()
        try:
            if id_name != None:
                cursor.execute(
                    f'''
                    SELECT {column}
                    FROM {table_name} 
                    WHERE 
                    id_name = ?
                    ''', (id_name,)
                )
                return cursor.fetchall()
            else:
                cursor.execute(
                    f'''
                    SELECT {column}
                    FROM {table_name} 
                    ''')
                return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def db_insert(self, table_name, id_name, user_name, user_language, learn_language, level_learn_language, file_log):
        conn = sqlite3.connect(f'{self.address_db}/{self.base_name}')
        cursor = conn.cursor()
        if not  self.db_reade(table_name, id_name):
            with conn:
                cursor.execute(f"""
                INSERT INTO {table_name} 
                (
                id_name,
                user_name,
                user_language,
                learn_language,
                level_learn_language, 
                file_log
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """, (id_name, user_name, user_language, learn_language, level_learn_language, file_log))
            cursor.close()
            conn.close()
        else:
            return None

    def __db_update(self, table_name, id_name, user_name, user_language, learn_language, level_learn_language, file_log):
        conn = sqlite3.connect(f'{self.address_db}/{self.base_name}')
        cursor = conn.cursor()
        with conn:
            cursor.execute(f"""
            UPDATE {table_name}
            SET
            id_name = ?,
            user_name = ?,
            user_language = ?,
            learn_language = ?,
            level_learn_language = ?,
            file_log = ?
            """, (id_name, user_name, user_language, learn_language, level_learn_language, file_log))
        cursor.close()
        conn.close()