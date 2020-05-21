from pprint import pprint

from pymongo import MongoClient

client = MongoClient()


def save_to_db(main_user, list_of_vkusers):

    this_user_db = client[f'{main_user.id}']
    list_of_best_suit = this_user_db['list_of_best_suit']

    for person in list_of_vkusers:

        person_dict = {'id': person.id,
                       'link': f'https://vk.com/id{person.id}',
                       'tree_photo': person.top_three_photo()
                       }
        list_of_best_suit.insert_one(person_dict)


def check_and_get_ids(main_user):
    base = client[f'{main_user.id}']
    collections = base.list_collection_names()

    if collections:
        print('база этого юзера уже есть')
        id_dict = list(base['list_of_best_suit'].find({}, {'id': 1, '_id': 0}))
        found_list = []
        for user in id_dict:
            found_list.append(user['id'])

        return found_list

    else:
        print('Для это юзера пару мы ещё не искали')
        empty_list = []
        return empty_list
