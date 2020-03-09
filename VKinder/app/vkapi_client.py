from VKinder.app.vkauth import get_vk_session


def get_user_data(user_id):
    """
    :param user_id: id пользователя или его screen_name
    :return: возвращает словарь с данными пользователя:
          -   'books': str,
              'can_access_closed': Bool,
              'city': {'id': int, 'title': str},
              'country': {'id': int, 'title': str},
              'first_name': str,
              'home_town': str,
              'id': int,
          -   'interests': str,
              'is_closed': Bool,
              'last_name': str,
          -   'movies': str,
          -   'music': str,
       *      'sex': int  # 0-не указан, 1-женский, 2-мужской
          -   'personal': {'alcohol': int,
                         - 'inspired_by': str,
                           'langs': list,
                           'life_main': int,
                           'people_main': int,
                           'political': int,
                         - 'religion': str,
                           'smoking': int}
    """

    vk = get_vk_session()
    fields = 'city, sex, books, country, home_town, interests, movies, music, personal'
    main_user_data = vk.users.get(user_ids=str(user_id), fields=fields)[0]
    # group_ids = vk.groups.get()['items']

    # pprint(main_user_data)
    return main_user_data


def search_people(main_user_sex, count):

    vk = get_vk_session()
    if main_user_sex == 1:
        sex_to_search = 2
    elif main_user_sex == 2:
        sex_to_search = 1
    else:
        sex_to_search = 0

    count = count
    sort = 0
    q = ''
    fields = 'city, sex, books, country, home_town, interests, movies, music, personal'

    search_res = vk.users.search(q=q, count=count, sort=sort, sex=sex_to_search, fields=fields)
    return search_res


if __name__ == '__main__':
    pass
