import requests


API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
wrong_api_key = 'SomWrongSetOfLetters'


def our_translator(apikey, url):

    text_to_translate = input('Введите текст для перевода')

    params = {'key': apikey,
              'text': text_to_translate,
              'lang': 'en-ru'}

    response = requests.get(url, params).json()

    return response


if __name__ == '__main__':
    print(our_translator(API_KEY, URL))
