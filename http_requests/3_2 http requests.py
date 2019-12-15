import requests
#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

def translate_it(file, file_to_write, from_lang, to_lang='ru'):
    """
    URL = https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :file: путь к файлу из которого переводим
    :file_to_write: путь к файлу в который записываем результат перевода
    :param to_lang: язык на который переводим
    :from_lang: язый с которого переводим
    :return: выводит сообщение о создании файла
    """

    with open(file, encoding='UTF8') as f:
        text_to_translate = f.read()

    params = {
        'key': API_KEY,
        'text': text_to_translate,
        'lang': '{}-{}'.format(from_lang, to_lang),
    }

    response = requests.get(URL, params=params)
    json_ = response.json()

    with open(file_to_write, 'w', encoding='UTF8') as ftw:
        ftw.write(' '.join(json_['text']))

    return f'Создан файл {file_to_write}'


if __name__ == '__main__':
    print(translate_it('fr.txt', 'ru_from_fr.txt', 'fr'))