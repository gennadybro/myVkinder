import os
import vk_api
import requests
import json
from vk_api.longpoll import VkLongPoll   # ???
from my_token import token, bad_token
from time import sleep
from random import randrange
# from bot import Vkbot as vkbot
vk_me = vk_api.VkApi(token=token, api_version='5.131').get_api()






def get_sex(sex_user):
    if sex_user == 2:
        find_sex = 1
        return find_sex
    elif sex_user == 1:
        find_sex = 2
        return find_sex
   

def user_search(SEX, BDATE, CITY, RELATION):
    print(SEX," : ", BDATE," : ",CITY," : ",RELATION)
    url = f'https://api.vk.com/method/users.search'
    params = {'access_token': bad_token,
            'v': '5.131',
            'sex': get_sex(SEX),
            'birth_year': BDATE,
            'city': CITY,
            'fields': 'is_closed, id, first_name, last_name,',
            'status': '1' or '6',
            'count': 500}
    resp = requests.get(url, params=params)
    resp_json = resp.json()
    print(resp_json)
    try:
        dict_1 = resp_json['response']
        list_1 = dict_1['items']
        filename = "Test"
        for person_dict in list_1:
            if person_dict.get('is_closed') == False:
                first_name = person_dict.get('first_name')
                last_name = person_dict.get('last_name')
                vk_id = str(person_dict.get('id'))
                vk_link = 'vk.com/id' + str(person_dict.get('id'))
                
                #                   блок временный
                if os.path.exists(f"{filename}"):
                    print(f"Директория существует")
                else:
                    os.mkdir(filename)
                with open(f"{filename}/{filename}.json", "w", encoding="utf-8") as file:
                    json.dump(resp_json, file, indent=4, ensure_ascii=False)

                #                       
                return first_name, last_name, vk_id, vk_link
            else:
                continue
        return f'Поиск завершён'
        print(first_name," ",last_name," ",vk_id," ",vk_link)
    except KeyError:
        write_msg(Vkbot.USER_ID, 'Ошибка получения токена')


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
        return list_of_ids
    except KeyError:
        write_msg(users_id, 'Ошибка получения токена')


# def username(user_id):   #  сбор информации о  пользователе
#     url = f'https://api.vk.com/method/users.get'
#     params = {'user_ids': user_id, 'fields': 'sex,bdate,city,relation', 'access_token' : token, 'v': '5.131'}
#     repl = requests.get(url, params=params)
#     response = repl.json()
#     print(response)
#     try:
#         information_dict = response['response']
#         for i in information_dict:
#             for key, value in i.items():
#                 first_name = i.get('first_name')
#                 relation = i.get('relation')
#                 wall_relation = i.get('is_closed')
#                 bdate = i.get('bdate')
#                 city = i.get('city')
#                 sex = i.get('sex')
#                 return  relation, first_name, bdate, city, sex, wall_relation
#     except KeyError:
#         write_msg(Vkbot.USER_ID, 'Ошибка получения токена, введите токен в переменную - my_token')


            