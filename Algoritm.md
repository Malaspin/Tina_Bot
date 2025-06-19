# Задача написать бота:

## Что мне нужно?

1. Сформулировать список переменных
   * username 
   * user_language
   * level_language  


2. Список где будут лежать переменные пользователя
    * Должны получить список в котором лежат словари с ключом username пример:  
    [{username:[{user_language:' '}, {level_language:' '}]]


3. Сформулировать функцию проверки наличия ключа по пользователю
    * def проверка(username):  
    в переменную из списка:  
    если username не принадлежит переменная:  
    то ДОБАВИТЬ  
    иначе:  
    принт ошибки (логин занят)
4. Сформулировать функцию добавления данных в список пользователя
   * def data_add (username):  
   user_language = input(Your native language)  
   level_language = input(Your language level)  
   user_dara.append({username:[{'user_language':user_language]},  
   {'level_language':level_language}})
5. Сформулировать функцию запроса у пользователя данных
6. Сформулировать функцию генерации промта
7. Сформулировать функцию для уточняющего запроса для пояснения
