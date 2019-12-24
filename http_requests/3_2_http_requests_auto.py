import requests
#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
DRIVE_API_KEY = 'AgAAAAAkrU39AADLW76HckcSYUJLolhAC5vWOJs'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
URL_for_lang_detect = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
URL_drive_path_request = 'https://cloud-api.yandex.net/v1/disk/resources/upload'


def translate_it(*files_to_translate, to_lang='ru'):
    """ Функция берёт каждый файл с текстом, указанный в параметре *files_to_translate, определяет
    его язык, переводит на указанный в параметре to_lang язык и сохраняет в файл
    с названием в формате from_<язык с которого переводим>_to_<язык на который переводим>.txt
    на компьютер пользователя и на яндекс диск пользователя

    параметры запроса для перевода:
    URL = https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    параметры запроса для автоопределения языка:
    https://translate.yandex.net/api/v1.5/tr.json/detect
     ? [key=<API-ключ>]
     & text=<текст>
     & [hint=<список вероятных языков текста>]
     & [callback=<имя callback-функции>]

    :*files_to_translate: пути к файлам из которых из которого переводим
    :to_lang: язык на который переводим

    """

    # цикл перебирает файлы, указанные в параметре files_to_translate
    for file in files_to_translate:
        with open(file, encoding='UTF8') as f:
            text_to_translate = f.read()

        # параметры для запроса на определение языка текста
        detect_params = {
            'key': API_KEY,
            'text': text_to_translate
        }

        # запрос для определения языка текста
        lang_detect_response = requests.get(URL_for_lang_detect, detect_params)
        from_lang = lang_detect_response.json()['lang']

        # параметры для запроса переводчику
        params = {
            'key': API_KEY,
            'text': text_to_translate,
            'lang': '{}-{}'.format(from_lang, to_lang)
        }

        # запрос переводчику
        response = requests.get(URL, params=params)

        # Подготовим текст для записи в файл
        json_ = response.json()
        text_for_file = ' '.join(json_['text']).encode('utf-8')

        # Параметры для запроса яндекс диску
        write_to_drive_params = {'path': f'from_{from_lang}_to_{to_lang}.txt',
                                 'overwrite': True
                                 }

        # Запросим путь для записи на яндекс-дикс
        drive_path = requests.get(URL_drive_path_request,
                                  write_to_drive_params,
                                  headers={'Authorization': DRIVE_API_KEY}
                                  )

        # записываем результат перевода в новый файл на компьютере
        with open(f'from_{from_lang}_to_{to_lang}.txt', 'w', encoding='UTF8') as ftw:
            ftw.write(' '.join(json_['text']))
            print(f'from_{from_lang}_to_{to_lang}.txt файл записан на диск')
#
        # Произведём запись на яндекс диск по предоставленному пути
        with open(f'from_{from_lang}_to_{to_lang}.txt', 'rb') as ftdw:
            print(f'from_{from_lang}_to_{to_lang}.txt файл открыт для чтения')

            requests.put(
                drive_path.json()['href'],
                data = ftdw
                )
            print(f'from_{from_lang}_to_{to_lang}.txt записан на яндекс-диск\n')



if __name__ == '__main__':
    translate_it('fr.txt', 'de.txt', 'es.txt', to_lang='ru')
