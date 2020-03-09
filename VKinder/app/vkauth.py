import vk_api
import json


def get_vk_session():

    vk_session = vk_api.VkApi()

    # Проверяем наличие файла с конфигом. если есть, то извлекаем токен
    try:
        with open('vk_config.v2.json', mode='r', encoding='utf8') as f:
            config = json.load(f)
            token = config['null']['token']['app6222115']['scope_140492255']['access_token']
            vk_session.token = {'access_token': token}
    except FileNotFoundError:
        pass

    # Проверяем валидность токена. Если он не устарел - авторизуемся
    if vk_session._check_token():
        print('success authorization with old token')
        return vk_session.get_api()

    # Если устарел - запрашиваем данные и авторизуемся заново
    else:
        vk_session.login = input('Введите логин: ')
        vk_session.password = input('Введите пароль: ')
        vk_session.auth()
        print('success authorization with new token')
        return vk_session.get_api()

#TODO: научить обрабатывать исключение при неправильном вводе пароля или имени пользователя