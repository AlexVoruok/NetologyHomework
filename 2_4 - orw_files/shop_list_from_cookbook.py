import json

cook_book = {}  # Словарь для хранения всеё кники рецептов
with open('recieps.txt', encoding='UTF8') as stream:
        while True:
            dish = stream.readline().strip()  # название блюда

            if not dish:  # Проверяем его существование, иначе - прерываем цикл
                break
            else:
                cook_book[dish] = []  # НАзвание блюда становится ключом словаря

            ingr_num = int(stream.readline())  #  Определяем, сколько раз ещё читаем строки, предже чем эта итерация закончится

            for ingr in range(ingr_num):
                ingredient = {}  # Словарь хранящий данные об определённом ингридиенте
                ingredient['ingridient_name'], ingredient['quantity'], ingredient['measure'] = stream.readline().strip().split(' | ')
                cook_book[dish].append(ingredient)  # Помещаем данные об ингридиенте в блюдо cook_book[dish]

            stream.readline()  # Пропускаем пустую строку


print(json.dumps(cook_book, ensure_ascii=False, indent=2))  # json используем для вывода в красивом виде


def get_shop_list_by_dishes(dishes, person_count):
    """
    :param dishes: список блюд из cook_book
    :param person_count: На сколько персон мы закупаем продукты
    :return: словарь с названием ингредиентов и его количества для блюда

    Пример вывода:
    {
    'Картофель': {'measure': 'кг', 'quantity': 2},
    'Молоко': {'measure': 'мл', 'quantity': 200},
    'Помидор': {'measure': 'шт', 'quantity': 4},
    'Сыр гауда': {'measure': 'г', 'quantity': 200},
    'Яйцо': {'measure': 'шт', 'quantity': 4},
    'Чеснок': {'measure': 'зубч', 'quantity': 6}
    }

    """
    shop_list = {}  # создаём словарь шоплист

    for dish in dishes:  # читаем блюдо
        for ingredient in cook_book[dish]:
            ingr_name = ingredient['ingridient_name']  # Название продукта для читаемости поместим в отдельную переменную
            shop_list.setdefault(ingredient['ingridient_name'], {})   # проверим наличие ключа с именем продукта, и если его нет, то в качестве значения присвоим ему пустой словарь
            shop_list[ingr_name]['measure'] = ingredient['measure']  # запишем название единицы измерения ингридиента в словарь
            # Проверим наличие данных о количестве ингридиента, и если его нет, присвоим 0 этому ключу и прибавим сюда количество по рецепту * количество людей
            shop_list[ingr_name]['quantity'] = shop_list[ingr_name].setdefault('quantity', 0) + int(ingredient['quantity'])*person_count

    return(json.dumps(shop_list, ensure_ascii=False, indent=2))  # json используем для вывода в красивом виде




menu = ', '.join(cook_book.keys())  # Создадим список блюд, которые есть у нас в книге рецептов

# Запросим у пользователя данные для подбора ингридиентов
dish_list = input(f'В нашей кулинарной книге есть следующие блюда: \n'
                  f'{menu} \n'
                  f'Какие из этих блюд вы хотите приготовить(Укажите через запятую)? \n').replace(' ','').title().split(',')

people = int(input('На сколько людей рассчитывать пир? \n'))

# Ловим исключение в случае отсутствующего блюда
try:
    print(get_shop_list_by_dishes(dish_list, people))

except KeyError as wrong_dish:
    print(f'Блюда {wrong_dish} нет в нашей книге рецептов. Смотрите внимательнее')
