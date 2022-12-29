from random import randrange

import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

from config import my_token, group_token
# from keyboards import keyboard

vk = vk_api.VkApi(token=group_token)  #Авторизация группы
longpoll = VkLongPoll(vk)
print("Бот создан")

def write_msg(user_id, message):  #  Отправка сообщений
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7)
    })

def uname(user_id):   #  имя пользователя
    url = f'https://api.vk.com/method/users.get'
    params = {'access_token': my_token,
              'user_ids': user_id,
              'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    print(response)
    try:
        information_dict = response['response']
        for i in information_dict:
            for key, value in i.items():
                first_name = i.get('first_name')
                return first_name
    except KeyError:
        write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - my_token')

def sender(user_id, text):
    vk.method('messages.send', {'user_id': user_id,
                                'message': text,
                                'random_id': 0})
                                 # 'keyboard': keyboard})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()
        sender(user_id, msg.lower())
        if request == "начинаем":
            write_msg(user_id, f"Привет, {uname((user_id))}")
        elif request == "вперёд":
            pass
        elif request == "стоп":
            write_msg(event.user_id, f"Досвидания, {uname(user_id)}")
            break
        else:
            write_msg(event.user_id, "Твоё сообщение непонятно")

