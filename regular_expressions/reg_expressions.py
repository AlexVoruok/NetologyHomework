import csv
import re
from pprint import pprint


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Храним все контакты в словаре
phone_book = {}

# Этим циклом разберём и упакуем в словарь данные. В качетве ключа словаря - фамилия.
# Остальные данные - список ['organization', 'position', 'phone', 'email']
for row in contacts_list:

    # Поскольку ФИО лежат кусками по разным колонкам, мы сначала соединим их в одну строку и поделим по пробелу
    name = f'{row[0]} {row[1]} {row[2]}'
    person = re.split(' ', name)

    family_name = person[0]
    name = person[1]
    surname = person[2]

    organize = row[3]
    pozition = row[4]
    phone = row[5]
    mail = row[6]

    try:
        # Если есть на что менять содержимое - меняем
        if name:
            phone_book[family_name][0] = name
        if surname:
            phone_book[family_name][1] = surname
        if surname:
            phone_book[family_name][2] = organize
        if surname:
            phone_book[family_name][3] = pozition
        if surname:
            phone_book[family_name][4] = phone
        if surname:
            phone_book[family_name][5] = mail

    # Если такой фамилии ещё нет в словаре - создаём
    except KeyError:
        phone_book[family_name] = [name, surname, organize, pozition, phone, mail]

pattern = re.compile(r'(\+7|8)\s?(\(?)(\d+)(\)?)(\s?|\-)(\d{1,3})(\s?|\-)'
                     r'(\d{1,2})(\s?|\-)(\d{1,2})((\s?|\-)(\(?)(доб\.)(\s?)(\d+)\)?)?')

# приведём в порядок телефоны
for value in phone_book.values():
    normallized = pattern.sub(r'+7(\3)\6-\8-\10 \14\16', value[4])
    value[4] = normallized.rstrip()

# приведём в порядок емайлы
for value in phone_book.values():
    value[5] = value[5].lower()

# подготовим данные для экспорта
contacts_list_edited = []
for key, value in phone_book.items():
    row = [key] + value
    contacts_list_edited.append(row)

# pprint(contacts_list_edited)

# сохраните получившиеся данные в другой файл

with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_edited)
