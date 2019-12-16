import requests
from pprint import pprint
import time
import json

# имя пользователя (eshmargunov) и id (171691064) - являются валидными входными данными.
access_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
URL = 'https://api.vk.com/method/'


class User:

    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_friends(self):
        """возвращает множество id друзей пользователя

        """
        friends_params = {'user_id': self.user_id,
                          'v': 5.8,
                          'access_token': access_token
                          }

        try:
            friends_response = requests.get(URL + 'friends.get', friends_params)
            friends_set = set(friends_response.json()['response']['items'])
            return friends_set
        except KeyError:
            error_msg = friends_response.json()['error']['error_msg']
            pprint(error_msg)

    def get_user_groups(self):
        """ возвращает множество id групп пользователя
            или ошибку если это действие недопустимо для пользователя


        """
        groups_params = {'user_id': self.user_id,
                         'v': 5.61,
                         'access_token': access_token,
                         # 'extended' : 1,
                         # 'fields' : 'name, member_count'
                         }

        groups_response = requests.get(URL + 'groups.get', groups_params)
        try:
            friends_set = set(groups_response.json()['response']['items'])
            return friends_set

        except KeyError:
            error_msg = groups_response.json()['error']['error_msg']
            if error_msg == 'Too many requests per second':
                try:
                    time.sleep(1.5)
                    groups_response = requests.get(URL + 'groups.get', groups_params)
                    friends_set = set(groups_response.json()['response']['items'])
                    return friends_set
                except KeyError:
                    error_msg = groups_response.json()['error']['error_msg']
                    return error_msg
            else:
                return error_msg

    def __str__(self):

        url = f'https://vk.com/id{self.user_id}'
        return url

    def unic_user_groups(self, friends_limit):
        """ Выдаёт перечень уникальных групп пользователя
            - в которых состоит он, но не состоит никто из его друзей
            параметр friends_limit ограничивает количество друзей, с кем проиходит сравнение

        """
        time.sleep(1)

        user_groups_set = self.get_user_groups()
        user_friends_set = self.get_user_friends()

        list_friends_instances = []
        for friend in user_friends_set:
            list_friends_instances.append(User(friend))

        unic_user_groups = user_groups_set

        friend_counter = 0  # ограничивающий счётчик

        for friend in list_friends_instances:
            friend_counter += 1
            try:
                # из множества групп пользователя убираем группы в которых состоит друг:
                get_user_groups_method_respond = friend.get_user_groups()
                unic_user_groups = unic_user_groups - get_user_groups_method_respond
                print('. user c id', friend.user_id, 'обработан')
            except TypeError:  # исключение вызывается когда пользователь ограничил доступ к своим группам
                print(f'Нет информации от пользователя https://vk.com/id{friend.user_id} ',
                      get_user_groups_method_respond)

            if friend_counter == friends_limit:
                break

        print(f'\nПользователь {john} имеет {len(unic_user_groups)} уникальных групп(ы): \n'
              + str(unic_user_groups) + '\n')

        return unic_user_groups


def get_group_info(group_id):
    """ Принимает на вход один id группы или список, возвращает словарь следующего содержания:
        “name”: “Название группы”,
        “gid”: “идентификатор группы”,
        “members_count”: количество_участников_сообщества

    """

    list_for_request = str(group_id)[1:-1]
    list_to_return = []

    gr_params = {'user_id': 3983782,
                 'v': 5.61,
                 'access_token': access_token,
                 'group_ids': list_for_request,
                 'fields': 'members_count'
                 }

    groups_response = requests.get(URL + 'groups.getById', gr_params)
    for group in groups_response.json()['response']:
        print('id: {}, Название: \n{}\nhttps://vk.com/{}\nКоличество пользователей: {}\n'.format(group['id'], group['name'], group['screen_name'], group['members_count'] ))
        group_dict = {"name": group['name'], "gid": group['id'], "members_count": group['members_count']}
        list_to_return.append(group_dict)

    return list_to_return


if __name__ == '__main__':

    john = User(171691064)

    unic_set = john.unic_user_groups(1000)

    dict_to_dump = get_group_info(unic_set)

    with open('groups.json', 'w', encoding='UTF-8') as ftw:
        json.dump(dict_to_dump, ftw, ensure_ascii=False, indent=2)
