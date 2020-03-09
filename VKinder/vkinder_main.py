"""
1. Модуль работы с апи
 -  Анализ/считывание данных о текущем пользователе - готово
 - Поиск других пользователей по заданным критериям - готово
2. Модуль с основной логикой - готово
4. Скачка топ3 популярных фото и информация о пользователе
5. Модуль загрузки в БД
6. Модуль тестирования

дипломное задание:
https://github.com/netology-code/py-advanced-diplom?fbclid=IwAR245WNmMvVpCnwQO5gYteNoEta5biavYxO7y_XCeXrlW1aRRaiuHwBYj-o

"""
from VKinder.app.vkapi_client import search_people, get_user_data
import re
from pprint import pprint

# Веса:
W_COUNTRY = 1
W_CITY = 50
W_HOME_TOWN = 300
W_LANGS = 30

W_COMMON_INTERESTS = 200
W_BOOKS = 80
W_MOVIES = 70
W_MUSIC = 60
W_INSPIRED_BY = 200
W_RELIGION = 50

W_ALCOHOL = 30
W_LIFE_MAIN = 40
W_PEOPLE_MAIN = 40
W_POLITICAL = 40

W_SMOKING = 40

# доля общих ключевых слов, после которой фактор начинает играть значение
PROP_COMMON_INTERESTS = 0.1
PROP_BOOKS = 0.1
PROP_MOVIES = 0.1
PROP_MUSIC = 0.1
PROP_INSPIRED_BY = 0.1
PROP_REGION = 0.1

# Поясняющие сообщения для ввода
MSG_POLITICAL = "Политические взгляды. " \
                "Целое число, Возможное значения: \n" \
                "1 — коммунистические; \n" \
                "2 — социалистические; \n" \
                "3 — умеренные; \n" \
                "4 — либеральные; \n" \
                "5 — консервативные; \n" \
                "6 — монархические; \n" \
                "7 — ультраконсервативные; \n" \
                "8 — индифферентные; \n" \
                "9 — либертарианские. \n"
MSG_PEOPLE_MAIN = "Главное в людях. " \
                  "Целое число, Возможное значения: \n" \
                  "1 — ум и креативность; \n" \
                  "2 — доброта и честность; \n" \
                  "3 — красота и здоровье; \n" \
                  "4 — власть и богатство; \n" \
                  "5 — смелость и упорство; \n" \
                  "6 — юмор и жизнелюбие. \n"
MSG_LIFE_MAIN = "Главное в жизни. " \
                "Целое число, Возможное значения: \n" \
                "1 — семья и дети; \n" \
                "2 — карьера и деньги; \n" \
                "3 — развлечения и отдых; \n" \
                "4 — наука и исследования; \n" \
                "5 — совершенствование мира; \n" \
                "6 — саморазвитие; \n" \
                "7 — красота и искусство; \n" \
                "8 — слава и влияние. \n"
MSG_SMOKING = "Отношение к курению: " \
              "Целое число, Возможное значения: \n" \
              "1 — резко негативное; \n" \
              "2 — негативное; \n" \
              "3 — компромиссное; \n" \
              "4 — нейтральное; \n" \
              "5 — положительное. \n"
MSG_ALCOHOL = "Отношение к алкоголю: " \
              "Целое число, Возможное значения: \n" \
              "1 — резко негативное; \n" \
              "2 — негативное; \n" \
              "3 — компромиссное; \n" \
              "4 — нейтральное; \n" \
              "5 — положительное. \n"


def make_keywords(string_to_prepare):
    """
    Преобразует строку в список ключевых слов
    """
    pattern = re.compile(r'\b[a-zA-Zа-яА-ЯёЁ]{2,6}')
    keywords_list = pattern.findall(string_to_prepare)

    lower_keywords_list = []

    # переведём все слова в нижний регистр
    for word in keywords_list:
        lower_keywords_list.append(word.lower())

    return set(lower_keywords_list)


def data_checker(data):
    # проверка наличия достаточного количества критериев для сравнения
    main_usr_data_values = list(data.values())
    # pprint(data)

    if data['sex'] == 0:
        data['sex'] = input('Укажите ваш пол в числовом отображении: 1-женский, 2-мужской')

    #  Если количество пустых полей больше заданного ниже значения, запустим запрос дополнительных данных
    n_of_full = 0
    for value in main_usr_data_values:
        if value:
            n_of_full += 1
    full_prop = int(round(n_of_full / len(main_usr_data_values), 1) * 100)

    if full_prop >= 70:
        return data
    else:
        print(f'Мало данных для поиска пары. Менее {full_prop}%. Для более точного поиска, '
              'пожалуйста, ответьте на дополнительные вопросы: \n')
        for key, value in data.items():
            if not value:
                if key in ['books', 'city', 'country', 'home_town', 'interests', 'movies',
                           'music', 'inspired_by', 'langs', 'religion']:
                    data[key] = make_keywords(input(f'Введите данные для {key} в текстовом формате: '))
                    print(data[key])

                # elif key == 'city':
                #     data[key] = input('Введите ваш город: ')
                #

                elif key == 'alcohol':
                    data[key] = input(MSG_ALCOHOL)
                elif key == 'life_main':
                    data[key] = input(MSG_LIFE_MAIN)
                elif key == 'people_main':
                    data[key] = input(MSG_PEOPLE_MAIN)
                elif key == 'political':
                    data[key] = input(MSG_POLITICAL)
                elif key == 'smoking':
                    data[key] = input(MSG_SMOKING)

        return data


class VKUser:
    raiting = 0

    def __init__(self, u_id, base_user=False, user_info=None):
        """
        :param u_id: id пользователя
        :param base_user: True, если создаваемые пользователь - тот, для кого мы будем искать пару
        :param user_info: словарь с атрибутеами пользователя в том случае, если base_user=False
        """

        if base_user:

            data = get_user_data(u_id)
            # Строки которые есть в данных об основном пользователи преобразуем
            # в список ключевых слов при помощи функции make_keywords
            # pprint(data)

            self.id = u_id
            self.sex = data['sex']
            self.first_name = data['first_name']
            self.last_name = data['last_name']

            self.country = data['country']['id'] if 'country' in data else None
            self.city = data['city']['id'] if 'city' in data else None
            self.home_town = data['home_town'] if 'home_town' in data else None

            self.interests = make_keywords(data['interests'])
            self.books = make_keywords(data['books'])
            self.movies = make_keywords(data['movies'])
            self.music = make_keywords(data['music'])

            if 'personal' in data:
                self.alcohol = data['personal'].get('alcohol')
                self.inspired_by = make_keywords(data['personal'].get('inspired_by', ''))
                self.langs = set(data['personal'].get('langs', []))
                self.life_main = data['personal'].get('life_main')
                self.people_main = data['personal'].get('people_main', '')
                self.political = data['personal'].get('political')
                self.religion = make_keywords(data['personal'].get('religion', ''))
                self.smoking = data['personal'].get('smoking')
            else:
                self.alcohol = None
                self.inspired_by = set()
                self.langs = set()
                self.life_main = None
                self.people_main = None
                self.political = None
                self.religion = set()
                self.smoking = None

            # проверка наличия достаточного количества критериев для сравнения
            data_checker(self.__dict__)
            # pprint(self.__dict__)

        else:
            # Строки которые есть в данных об основном пользователи преобразуем
            # в список ключевых слов при помощи функции make_keywords

            self.id = u_id
            self.sex = user_info['sex']
            self.first_name = user_info['first_name']
            self.last_name = user_info['last_name']

            self.country = user_info['country']['id'] if 'country' in user_info else None
            self.city = user_info['city']['id'] if 'city' in user_info else None
            self.home_town = user_info['home_town'] if 'home_town' in user_info else None

            self.interests = make_keywords(user_info.get('interests', ''))
            self.books = make_keywords(user_info.get('books', ''))
            self.movies = make_keywords(user_info.get('movies', ''))
            self.music = make_keywords(user_info.get('music', ''))

            if 'personal' in user_info:
                self.alcohol = user_info['personal'].get('alcohol')
                self.inspired_by = make_keywords(user_info['personal'].get('inspired_by', ''))
                self.langs = set(user_info['personal'].get('langs', []))
                self.life_main = user_info['personal'].get('life_main')
                self.people_main = user_info['personal'].get('people_main', '')
                self.political = user_info['personal'].get('political')
                self.religion = make_keywords(user_info['personal'].get('religion', ''))
                self.smoking = user_info['personal'].get('smoking')
            else:
                self.alcohol = None
                self.inspired_by = set()
                self.langs = set()
                self.life_main = None
                self.people_main = None
                self.political = None
                self.religion = set()
                self.smoking = None

    def __repr__(self):
        url = f'https://vk.com/id{self.id}'
        return f"{self.first_name} {self.last_name}, рейтинг: {self.raiting} \n {url} \n"

    def __str__(self):
        url = f'https://vk.com/id{self.id}'
        return f"{self.first_name} {self.last_name}, рейтинг: {self.raiting} \n {url} \n"

    def compare(self, candidate):
        """
        Сравнивает два объекта класса VKUser по всем параметрам и рассчитывает рейтинг
        """

        # совпадение строк ***************************************
        # Страна
        if self.country == candidate.country:
            candidate.raiting += W_COUNTRY

        # Город
        if self.city == candidate.city:
            candidate.raiting += W_CITY

        # Родной город
        if self.home_town == candidate.home_town:
            candidate.raiting += W_HOME_TOWN

        # частичное совпадение списка строк *********************
        # Интересы
        common_interests = self.interests & candidate.interests  # общие интересы
        if common_interests:
            common_part = len(common_interests)/len(self.interests)  # доля общих интересов от всех интересов
            if common_part >= PROP_COMMON_INTERESTS:
                candidate.raiting += W_COMMON_INTERESTS

        # Книги
        common_books = self.books & candidate.books  # общие книги
        if common_books:
            common_part = len(common_books) / len(self.books)  # доля общих книг от всех книг
            if common_part >= PROP_BOOKS:
                candidate.raiting += W_BOOKS

        # Кино
        common_movies = self.movies & candidate.movies  # общие фильмы
        if common_movies:
            common_part = len(common_movies) / len(self.movies)  # доля общих фильмов от всех фильмов
            if common_part >= PROP_MOVIES:
                candidate.raiting += W_MOVIES

        # Музыка
        common_music = self.music & candidate.music  # общая музыка
        if common_music:
            common_part = len(common_music) / len(self.music)  # доля общей музыки от всехй музыки
            if common_part >= PROP_MUSIC:
                candidate.raiting += W_MUSIC

        # inspired_by
        common_inspired = self.inspired_by & candidate.inspired_by  # общее вдохновляющее
        if common_inspired:
            common_part = len(common_inspired) / len(self.inspired_by)  # доля общего вдохновл во всём вдохновляющ
            if common_part >= PROP_INSPIRED_BY:
                candidate.raiting += W_INSPIRED_BY

        # Религия
        common_religion = self.religion & candidate.religion  # общее в религии
        if common_religion:
            common_part = len(common_religion) / len(self.religion)  # доля общего в религии от всей религии
            if common_part >= PROP_REGION:
                candidate.raiting += W_RELIGION

        # пересечение списка строк *******************************
        # Языки
        if len(self.langs & candidate.langs) >= 2:
            candidate.raiting += W_LANGS

        # совпадение значений *******************************
        if self.alcohol == candidate.alcohol:
            candidate.raiting += W_ALCOHOL
        if self.life_main == candidate.life_main:
            candidate.raiting += W_LIFE_MAIN
        if self.people_main == candidate.people_main:
            candidate.raiting += W_PEOPLE_MAIN
        if self.political == candidate.political:
            candidate.raiting += W_POLITICAL
        if self.smoking == candidate.smoking:
            candidate.raiting += W_SMOKING

    def seek_for_pair_and_estimate(self, count, list_number=10):
        """
        Делает поиск заданного количества пользователей ВК используя метод search_people
        помещает найдённых кандидатов в множество и
        используя метод compare рассчитывает рейтинг для них
        выводит первые list_number с максимальным рейтингом
        """
        pair_set = set()
        search_res = search_people(self.sex, count, self.city)
        # pprint(search_res)
        for man in search_res['items']:
            # pprint(man)
            m_id = man['id']
            this_man = VKUser(m_id, user_info=man)
            pair_set.add(this_man)
            # pprint(this_man.__dict__)
            self.compare(this_man)
        pprint(sorted(pair_set, key=lambda x: x.raiting, reverse=True)[0:list_number])

        # pprint(search_res)


if __name__ == '__main__':

    main_user = VKUser('ssg1712', base_user=True)

    main_user.seek_for_pair_and_estimate(1000, 3)

# TODO Учесть возраст при поиске
# если что-то сломается с ключевыми словами - проверить влияние set в make_keywords
