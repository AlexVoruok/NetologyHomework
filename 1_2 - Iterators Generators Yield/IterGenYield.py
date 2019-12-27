import json
import hashlib


class LinkMaker:

    def __init__(self, source, domain, startcounter=0):
        self.source = source
        self.domain = domain
        self.counter = startcounter

    def __iter__(self):
        return self

    def __next__(self):
        try:
            country = self.source[self.counter]['name']['official'].replace(' ', '_')
            genlink = f'{self.domain}{country}'
            rusname = self.source[self.counter]['translations']['rus']['common']
            data_to_write = f'{rusname} - {genlink}'
            self.counter += 1
            return data_to_write

        except IndexError:
            raise StopIteration

# Первая версия:

# def hash_generator(path):
#     with open(path, encoding='utf-8') as readfile:
#         iterator = readfile.__iter__()
#         nextstring = iterator.__next__().rstrip()  # Уберём перенос строки
#         try:
#             while True:
#                 hashmd5 = hashlib.md5(nextstring.encode('utf-8')).hexdigest()
#                 yield hashmd5, nextstring
#                 nextstring = iterator.__next__().rstrip()  # Уберём перенос строки
#         except StopIteration:
#             pass

def hash_generator(path):
    with open(path, encoding='utf-8') as readfile:
        while True:
            nextstring = readfile.readline().rstrip()
            if nextstring == '':
                break
            hashmd5 = hashlib.md5(nextstring.encode('utf-8')).hexdigest()
            yield hashmd5, nextstring




if __name__ == '__main__':

    with open('countries.json', 'r') as f:
        sourcedata = json.load(f)

    # передаём файловый объект генератору ссылок и записываем результат в новый файл
    with open('country_wikilinks.txt', 'w', encoding='utf-8') as wikilinks:
        for link in LinkMaker(sourcedata, 'https://wikipedia.org/wiki/'):
            print(link)
            wikilinks.write(link + '\n')

    # для каждой строки полученного выше файла генерируем хэш-сумму и выводим на экран
    for hash_string, string in hash_generator('country_wikilinks.txt'):
        print(f'хеш {hash_string} - для строки "{string}"')
