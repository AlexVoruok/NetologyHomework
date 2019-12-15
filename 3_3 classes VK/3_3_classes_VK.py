import requests
from pprint import pprint

# client_id приложения
client_id = '7243717'

# сервисный ключ доступа
service_token = 'e799671fe799671fe799671f4ce7f7e0daee799e799671fba685f9aaa61747aaf1d1fc4'

# url для запроса друзей friends.get
URL_friends_get = 'https://api.vk.com/method/friends.get'

class User():

    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_friends(self):
        '''
        возвращает множество id друзей пользователя
        '''
        params = {'user_id': self.user_id,
                  'v' : 5.89,
                  'access_token' : service_token,
                  'fields':'name',
                  'order': 'name'
                 }
        userget = requests.get(URL_friends_get, params)
        #pprint(userget.json()['response']['items'])

        friends_set = set()

        for dict in userget.json()['response']['items']:
            # для заполнения словаря friends_set[dict['id']] = [dict['first_name'], dict['last_name']]
            friends_set.add(dict['id'])

        return friends_set

    def user_url(self):
        '''
        Возвращает ссылку на профиль пользователя
        '''
        url = f'https://vk.com/id{self.user_id}'
        return print(url)

    def __and__(self, IDuser2):

        """
        Принимает на вход id пользователя с которым требуется найти общих друзей
        возвращает список общих друзей этих двух пользователей
        где каждый элемент списка - экземпляр класса User
        Выводит сообщение, если мы пытаемся сравнитьсписки пользователей с самим же собой
        """

        # создадим экземляры класса
        user1 = self
        user2 = IDuser2

        # выявим пересечение множеств друзей пользователей и сделаем из этого список
        if self.user_id != user2.user_id:
            common_friends = list(user1.get_user_friends()&user2.get_user_friends())

            print(f'Количество общих друзей - {len(common_friends)}\n')

            # Создадим список общих друзей пользователей, состоящий из экземпляров класса User
            list_common_friends_classes = []
            for user in common_friends:
                list_common_friends_classes.append(User(user))
            return pprint(list_common_friends_classes)

        else:
            error = 'В качестве объекта для сравнениея вы ввели пользователя с тем же самым ID. \n' \
                    'Для корректной работы функции common_friends_list требуется ввести ID другого пользователя'
            return pprint(error)

    def __str__(self):

        url = f'https://vk.com/id{self.user_id}'
        return url




if __name__ == '__main__':

    alex = User(2553860)
    some = User(4679683)

    # Ссылка на профиль пользователя
    print(alex)

    # общие друзия с пользователем 4679683
    alex&some
    print('\n')

    # опопытаемся сравнить списки друзей с самим собой
    alex&alex


