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
            if not list(db.find(row)):
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

    # получим список слов, которые мы будем искать в базе без пробелов и знаков препинания
    pattern = '\\w+'
    words_to_find = re.findall(pattern, name)

    # поищем каждое слово из сформированного списка в базе и выведем результат
    printed_list = []  # список для хранения названия группы, которые мы уже вывели на печать
    for word in words_to_find:
        regex = re.compile(word, re.IGNORECASE)
        result = db.find({'Исполнитель': {'$regex': regex}})

        # Выведем результат только в том случае, если мы его ранее не выводили
        for row in result:
            if row['Исполнитель'] not in printed_list:
                print('Исполнитель:', row['Исполнитель'])
                print('Цена', row['Цена'])
                print('Место', row['Место'])
                print('Дата', row['Дата'])
                print()
                printed_list.append(row['Исполнитель'])


if __name__ == '__main__':

    mongo_client = MongoClient()
    ticket_db = mongo_client['ticket_db']
    this_city_base = ticket_db['this_city_base']
    # this_city_base.delete_many({})

    read_data('artists.csv', this_city_base)

    find_cheapest(this_city_base)

    singer = input('\nВведите имя исполнителя для поиска билетов: ')
    find_by_name(singer, this_city_base)
