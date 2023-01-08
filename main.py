import vk_api
import requests
import sqlalchemy
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from urllib.parse import urlparse, urlencode
from config import token, group_token, token, userdb, passworddb
from database import add_my_data, add_parthers_data
# from vksearch import  user_search, write_msg
# from keyboards import keyboard

print("Бот создан")
class Vkbot:
    BASE_URL = "https://api.vk.com/method"   #  наверно избыточно 
    METOD_USER_SEARCH = "users.search"       #
    PROTOCOL_VERSION: str = "5.131"
    SEARCH = []
    SEX = None
    BDATE = None
    CITY = None
    RELATION = None
    USER_ID = None
    vk = vk_api.VkApi(token=group_token)  #Авторизация группы
    longpoll = VkLongPoll(vk)
    vk_me = vk_api.VkApi(token=token, api_version='5.131').get_api()
    LIST_USERS = []


def write_msg(user_id, message):  #  Отправка сообщений
    Vkbot.vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7)
    })


def username(user_id):   #  сбор информации о  пользователе
    url = f'https://api.vk.com/method/users.get'
    params = {'user_ids': user_id, 'fields': 'sex,bdate,city,relation', 'access_token' : token, 'v': '5.131'}
    repl = requests.get(url, params=params)
    response = repl.json()
    try:
        information_dict = response['response']
        for i in information_dict:
            for key, value in i.items():
                first_name = i.get('first_name')
                last_name = i.get('last_name')
                relation = i.get('relation')
                wall_relation = i.get('is_closed')
                bdate = i.get('bdate')
                city = i.get('city')
                user_sex = i.get('sex')
                date_year = int(bdate[-4:])
                # add_my_data(user_id, first_name, last_name, date_year, city["title"], user_sex, relation)
                return  relation, first_name, last_name, date_year, city, user_sex, wall_relation                         #   Пересмотреть подход
    except KeyError:
        write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - token')


def user_search(SEX, BDATE, CITY, RELATION):
    print(SEX," : ", BDATE," : ",CITY," : ",RELATION)
    url = f'https://api.vk.com/method/users.search'
    params = {'access_token': token,
            'v': '5.131',
            'sex': 1, # if SEX == '1' else 2,
            'birth_year': BDATE,
            'city': CITY,
            'fields': 'is_closed, id, first_name, last_name,',
            'status': '1' or '6',
            'count': 500}
    resp = requests.get(url, params=params)
    resp_json = resp.json()
    # print(resp_json)
    try:
        dict_1 = resp_json['response']
        list_1 = dict_1['items']
        # filename = "Test"
        for person_dict in list_1:
            if person_dict.get('is_closed') == False:
                first_name = person_dict.get('first_name')
                last_name = person_dict.get('last_name')
                vk_id = str(person_dict.get('id'))
                vk_link = 'vk.com/id' + str(person_dict.get('id'))
                add_parthers_data(first_name, last_name, vk_id, vk_link, Vkbot.USER_ID)
                # Vkbot.LIST_USERS.append({first_name, last_name, vk_id, vk_link}) 
            else:
                continue
               
        # print(Vkbot.LIST_USERS)
        return f'Поиск завершён'
        
    except KeyError:
        write_msg(Vkbot.USER_ID, 'Ошибка получения токена')




# def message_result_find(user_id):
#     Vkbot.vk.method('messages.send', 
#             {'user_id': user_id,
#             'access_token': token_foto,
#             'message': message,
#             'attachment': f'photo{self.person_id(offset)}_{self.get_photo_3(self.person_id(offset))}',
#             'random_id': 0})


def get_sex(sex_user):
    if sex_user == 2:
        find_sex = 1
        return find_sex
    elif sex_user == 1:
        find_sex = 2
        return find_sex


def get_foto_users(users_id):
    url = 'https://api.vk.com/method/photos.getAll'
    params = {'access_token': token,
                'type': 'album',
                'owner_id': users_id,
                'extended': 1,
                'count': 25,
                'v': '5.131'}
    resp = requests.get(url, params=params)
    dict_photos = dict()
    resp_json = resp.json()
    try:
        dict_1 = resp_json['response']
        list_1 = dict_1['items']
        for i in list_1:
            photo_id = str(i.get('id'))
            i_likes = i.get('likes')
            if i_likes.get('count'):
                likes = i_likes.get('count')
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        print(list_of_ids)
        return list_of_ids
    except KeyError:
        write_msg(users_id, 'Ошибка получения токена')


def get_photo_1(users_id):
    """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ № 1"""
    list = get_foto_users(users_id)
    count = 0
    for i in list:
        count += 1
        if count == 1:
            return i[1]


def get_photo_2(users_id):
    """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ № 2"""
    list = get_foto_users(users_id)
    count = 0
    for i in list:
        count += 1
        if count == 2:
            return i[1]

def get_photo_3(users_id):
    """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ № 3"""
    list = get_foto_users(users_id)
    count = 0
    for i in list:
        count += 1
        if count == 3:
            return i[1]


def send_photo_1(user_id, message, offset):
    """ОТПРАВКА ПЕРВОЙ ФОТОГРАФИИ"""
    Vkbot.vk.method('messages.send', {'user_id': user_id,
                                        'access_token': token_foto,
                                        'message': message,
                                        'attachment': f'photo{person_id(offset)}_{get_photo_1(person_id(offset))}',
                                        'random_id': 0})


def send_photo_2(self, user_id, message, offset):
    """ОТПРАВКА ВТОРОЙ ФОТОГРАФИИ"""
    Vkbot.vk.method('messages.send', {'user_id': user_id,
                                        'access_token': token_foto,
                                        'message': message,
                                        'attachment': f'photo{self.person_id(offset)}_{self.get_photo_2(self.person_id(offset))}',
                                        'random_id': 0})


def send_photo_3(self, user_id, message, offset):
    """ОТПРАВКА ТРЕТЬЕЙ ФОТОГРАФИИ"""
    Vkbot.vk.method('messages.send', {'user_id': user_id,
                                        'access_token': token_foto,
                                        'message': message,
                                        'attachment': f'photo{self.person_id(offset)}_{self.get_photo_3(self.person_id(offset))}',
                                        'random_id': 0})


for event in Vkbot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()
        Vkbot.RELATION, first_name, last_name, Vkbot.BDATE, Vkbot.CITY, Vkbot.SEX, wall_relation = username(user_id)
        Vkbot.USER_ID = user_id
      
        offset = 0
        if request == "привет":
            write_msg(user_id, f"Здравствуйте, {first_name}, добро пожаловать в бот \n  для поиска наберите: start")       
        elif request == "start":
            if wall_relation == True:
                write_msg(user_id, "Ваша страница закрыта")
            else:
                # if bdate = None
                    
                #     #   Vkbot.BDATE = int(bdate[-4:])   #  вывод года (1900) из полной даты (01.01.1900)
                # write_msg(user_id, f"Отлично. давайте подберем для Вас пару. \n Ваш год рождения, {Vkbot.BDATE}")
                if Vkbot.CITY == None:
                    write_msg(user_id, "В вашем пофиле не указан город, \n заполните профиль и попробуйте еще раз")
                    break
                else:
                    if Vkbot.SEX == '1':
                        sex,find_sex = "мужчину",2
                    else:
                        sex,find_sex = "женщину",1
                    city_id, city = Vkbot.CITY["id"], Vkbot.CITY["title"]
                    write_msg(user_id, f"Ищем в г.,{city}, {sex}") 
                    print(user_id, first_name, last_name, Vkbot.BDATE, city, Vkbot.SEX, Vkbot.RELATION)   #  врременно
                    add_my_data(user_id, first_name, last_name, Vkbot.BDATE, city, Vkbot.SEX, Vkbot.RELATION)               
                    user_search(Vkbot.SEX,Vkbot.BDATE,city_id,Vkbot.RELATION)
                    # foto = get_foto_users(vk_id)
                    # write_msg(user_id, f"Вот что нашлось:  {first_name}, {last_name}, {vk_link}")    
                    # send_photo_1(vk_id, "фото", offset)
        elif request == "next":
            offset += 1
            # first_name, last_name, vk_id, vk_link =  user_search(Vkbot.SEX,Vkbot.BDATE,city_id,Vkbot.RELATION)
            foto = get_foto_users(vk_id)
            # write_msg(user_id, f"Вот что нашлось:  {first_name} ,{last_name} , {vk_id} , {vk_link}, {foto}")    
            # send_photo_1(user_id, "Первое фото", offset)

        elif request == "stop":
            write_msg(user_id, f"До свидания, {first_name}")
            
            break
        else:
            # Vkbot.RELATION, myname, bdate, Vkbot.CITY, Vkbot.SEX, wall_relation = username(user_id)
            # Vkbot.USER_ID = user_id
            write_msg(user_id, f"Здравствуйте, {first_name}, добро пожаловать в бот \n  для поиска наберите start.")  