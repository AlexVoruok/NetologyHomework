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
