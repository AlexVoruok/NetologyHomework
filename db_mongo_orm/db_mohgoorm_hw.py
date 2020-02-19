import csv
import re
from pymongo import MongoClient


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """

    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Переведём цену в целочисленный вид
            row['Цена'] = int(row['Цена'])

            # ПРоверим наличие этих данных в ДБ и запишем если нет
            if list(db.find(row)):
                pass
            else:
                db.insert_one(row)
                print('row added')


def find_cheapest(db):
    """
    Отсортировать билеты из базы по возрастанию цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """
    print('Отсортировано по цене:')
    for row in db.find().sort('Цена', -1):
        print('Исполнитель: ', row['Исполнитель'],
              'Цена: ', row['Цена'])


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке, например "Seconds to"),
    и вернуть их по возрастанию цены
    """

    # regex = re.compile('укажите регулярное выражение для поиска. ' \
    #                    'Обратите внимание, что в строке могут быть специальные символы, их нужно экранировать')

    pattern = "[\\w]+"

    names_to_search = re.findall(pattern, name.lower())

    # print(names_to_search)

    for concert in db.find():
        names_to_check = re.findall(pattern, concert['Исполнитель'].lower())
        # print(names_to_check)

        if set(names_to_search) & set(names_to_check):
            print('Исполнитель:', concert['Исполнитель'])
            print('Цена', concert['Цена'])
            print('Место', concert['Место'])
            print('Дата', concert['Дата'])


if __name__ == '__main__':

    mongo_client = MongoClient()
    ticket_db = mongo_client['ticket_db']
    this_city_base = ticket_db['this_city_base']
    # this_city_base.delete_many({})

    read_data('artists.csv', this_city_base)

    find_cheapest(this_city_base)

    singer = input('\nВведите имя исполнителя для поиска билетов: ')
    find_by_name(singer, this_city_base)
