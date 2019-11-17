import json

cook_book = {}
with open('recieps.txt', encoding='UTF8') as stream:
        while True:
            dish = stream.readline().strip()
            if not dish:
                break
            else:
                cook_book[dish] = []
            ingr_num = int(stream.readline())
            # print(range(ingr_num))
            for ingr in range(ingr_num):
                ingredient = {}
                ingredient['ingridient_name'], ingredient['quantity'], ingredient['measure'] = stream.readline().strip().split(' | ')
                cook_book[dish].append(ingredient)

            stream.readline()


print(json.dumps(cook_book, ensure_ascii=False, indent=2))