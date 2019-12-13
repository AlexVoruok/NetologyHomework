import requests
from pprint import pprint
import time

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

        friends_response = requests.get(URL + 'friends.get', friends_params)
        friends_set = set(friends_response.json()['response']['items'])

        return friends_set

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

    def user_url(self):
        """ Возвращает ссылку на профиль пользователя

        """
        url = f'https://vk.com/id{self.user_id}'
        return url

    def common_friends_list(self, iduser2):
        """ Принимает на вход id пользователя с которым требуется найти общих друзей
        возвращает список общих друзей этих двух пользователей
        где каждый элемент списка - экземпляр класса User
        Выводит сообщение, если мы пытаемся сравнитьсписки пользователей с самим же собой

        """

        # создадим экземляры класса
        user1 = self
        user2 = User(iduser2)

        # выявим пересечение множеств друзей пользователей и сделаем из этого список
        if self.user_id != user2.user_id:
            common_friends = list(user1.get_user_friends() & user2.get_user_friends())

            print(f'Количество общих друзей - {len(common_friends)}\n')

            # Создадим список общих друзей пользователей, состоящий из экземпляров класса User
            list_common_friends_classes = []
            for user in common_friends:
                list_common_friends_classes.append(User(user))
            return list_common_friends_classes

        else:
            error = 'В качестве объекта для сравнениея вы ввели пользователя с тем же самым ID. \n' \
                    'Для корректной работы функции common_friends_list требуется ввести ID другого пользователя'
            return error


if __name__ == '__main__':
    # создадим нашего тестового пользоваьеля
    john = User(171691064)

    # множество id групп пользователя
    user_set_groups = john.get_user_groups()
    # pprint(user_set_groups)

    # Множество id друзей пользователя
    user_friends_set = john.get_user_friends()
    # pprint(user_friends_set)

    # Создаём список друзей пользователя в виде экземпляров класса User
    list_friends_instances = []
    for friend in user_friends_set:
        list_friends_instances.append(User(friend))
    # pprint(list_friends_instances)

    # Создадим множество уникальных групп пользователя от которого мы далее
    # будем отсекать группы в которых состоят его друзья
    unic_user_groups = user_set_groups

    i = 0  # ограничивающий счётчик

    # перебираем друзей пользователя
    for friend in list_friends_instances:
        i += 1
        try:
            # pprint(friend.get_user_groups())
            # из множества групп пользователя убираем группы в которых состоит друг:
            get_user_groups_method_respond = friend.get_user_groups()
            unic_user_groups = unic_user_groups - get_user_groups_method_respond
            print('. user c id', friend.user_id, 'обработан')
        except TypeError:  # исключение вызывается когда пользователь ограничил доступ к своим группам
            print(f'Нет информации от пользователя https://vk.com/id{friend.user_id} ', get_user_groups_method_respond)

        # if i == 5:  # сервисный инструмент, который ограничивает число итераций
        #     break

    print(f'\nПеречень уникальных групп пользователя {john.user_url()}: \n', unic_user_groups)


# Вывод информации о группах из перечня уникальных групп:
    list_for_request = ''
    for group in list(unic_user_groups):
        list_for_request += str(group)+', '

    pararams = {'user_id': 3983782,
                'v': 5.61,
                'access_token': access_token,
                'group_ids': list_for_request,
                }

    groups_response = requests.get(URL + 'groups.getById', pararams)
    for group in groups_response.json()['response']:
        print('id: {}, Название: \n{}\nhttps://vk.com/{}\n'.format(group['id'], group['name'], group['screen_name']))

