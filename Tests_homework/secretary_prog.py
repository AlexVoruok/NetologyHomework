from Tests_homework.data_base import directories, documents

# Сообщение об отсутствующем документе
warning_doc_num = ("\nДокумента с таким номером не существует \n"
                   "Чтобы добавить новый документ используйте команду 'a' \n")

# Сообщение об отсутствующей полке
warning_shelf = ('\nПолки с таким номером не существует. \nДействие не выполнено.'
                 '\nПопробуйте ещё раз \n ')

# Инстркуция о командах для пользователя:
instruct = 'Список команд: \n '\
      'p - найти имя человека по номеру документа \n '\
      'l - посмотреть список всех документов \n '\
      's - найти, на какой полке лежит документ с определённым номером \n '\
      'a - добавить новый документ \n '\
      'd - удалить документ \n '\
      'm - переместить документ \n '\
      'as - добавить новую полку с указанным номером \n '\
      'ado - вывести перечень всех владельцев документов в нашей базе \n '\
      'q - завершить сеанс \n'


def people_by_number():
    """ Функция для команды 'p', которая спросит номер документа
    и выведет имя человека, которому он принадлежит

    """
    doc_number = input('Введите номер документа: ')
    exist = False  # Эта переменная поможет вывести предупреждение, если такого документа нет
    # Проверяем наличие документа и выводим имя человека
    for doc in documents:
        if doc['number'] == doc_number:
            exist = True
            try:
                print(doc['name'], '\n')
            except KeyError:
                print(f'Для документа {doc_number} не указан владелец\n')
    if not exist:
        print(warning_doc_num)
        value = 'hi'


def all_doc_list():
    """ Функция для команды 'l', которая выведет список всех документов
    в формате passport "2207 876234" "Василий Гупкин"

    """
    for doc in documents:
        try:
            doc["name"]
        except KeyError:
            doc["name"] = ''
        finally:
            print(f' {doc["type"]:12}  "{doc["number"]}"   "{doc["name"]}"')


def doc_shell_find():
    """ Функция для команды 's', которая спросит номер документа и выведет номер полки,
    на которой он находится

    """
    doc_number = input('Введите номер документа: ')
    exist = False  # Эта переменная поможет вывести предупреждение, если такого документа нет
    for shelf in directories.keys():
        if doc_number in directories[shelf]:
            print(f'Этот документ лежит на полке {int(shelf)}')
            exist = True
    if not exist:
        print(warning_doc_num)


def add_new_doc():
    """ Функция для 'a' - команды, которая добавит новый документ в каталог и в перечень полок,
    спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться

    """
    new_doc_number = input('Введите номер нового документа: ')
    new_doc_type = input('Введите тип нового документа: ')
    new_doc_name = input('Введите имя владельца нового документа: ')
    new_doc_shelf = input('Укажите полку, на которой будет хранится новый документ: ')

    # Эта переменная для того чтобы показать пользователю актуальный набор полок
    shelf_list = ', '.join(list(directories.keys()))

    # Проверяем существование полки и добавляем, если она существует
    if new_doc_shelf in directories.keys():
        documents.append({'type': new_doc_type, 'number': new_doc_number, 'name': new_doc_name})
        directories[new_doc_shelf].append(new_doc_number)
        print(f'\nДокумент с номером {new_doc_number} добавлен на полку {new_doc_shelf} \n')
    else:
        print(warning_shelf, f'\nСейчас есть полки с номерами {shelf_list}')


def del_doc():
    """Функция для 'd' - команды, которая
    спросит номер документа и удалит его из каталога и из перечня полок

    """
    doc_to_del = input('Введите номер документа, который нужно удалить: ')

    exist = False  # Эта переменная поможет вывести предупреждение, если такого документа нет
    for doc in documents:
        if doc['number'] == doc_to_del:
            documents.remove(doc)
            exist = True
            for shelf in directories.keys():
                if doc_to_del in directories[shelf]:
                    directories[shelf].remove(doc_to_del)
            print(f'Документ c номером {doc_to_del} удалён из базы. \n')

    if not exist:
        print(warning_doc_num)


def doc_move():
    """ Функция для команды 'm' - которая спросит номер документа и
    целевую полку и переместит его с текущей полки на целевую

    """
    doc_tomove_number = input('Введите номер перемещаемого документа: ')

    doc_exist = False  # Эта переменная поможет вывести предупреждение, если такого документа нет
    old_shelf_list = []  # Эта переменная нужна на тот случай, если документ оказался зарегистрирован на нескольких полках
    shelf_list = ', '.join(
        list(directories.keys()))  # Эта переменная для того чтобы показать пользователю актуальный набор полок

    # Проверим сначала наличие документа
    for shelf in directories.keys():
        for doc in directories[shelf]:
            if doc_tomove_number == doc:
                old_shelf_list.append(shelf)
                doc_exist = True

    # Запрос номера полки, проверка её наличия, удаления с текущей полки и помещение на новую при условии наличия док-та
    if doc_exist:
        shelf_to_put_on = input('Укажите номер полки, куда переместить: ')
        if shelf_to_put_on in directories.keys():
            for shelf in old_shelf_list:  # Этот цикл уберёт все лишние записи если документ оказался записан на нескольких полках
                directories[shelf].remove(doc_tomove_number)
            directories[shelf_to_put_on].append(doc_tomove_number)

            print(f'документ "{doc_tomove_number}" перемещён на полку {shelf_to_put_on} \n')
        else:
            print(warning_shelf)
    else:
        print(warning_doc_num, f'\nСейчас есть полки с номерами {shelf_list}')


def make_new_shelf():
    """ Функция для команды 'as' - команда, которая спросит номер новой полки и добавит ее в перечень

    """
    new_shelf_num = input('Введите номер новой полки: ')
    if new_shelf_num not in directories.keys():
        directories[new_shelf_num] = []
        print(f'Новая полка с номером {new_shelf_num} создана \n')
    else:
        print('Полка с таким номером уже существует \n')

def all_doc_owners():
    """ Эта функция выводит имена всех владельцев документов из списка документов.
        Если у документа пустое с именем или это поле вообще отсутствует - ловим это исключение
        и выводим сообщение для пользователя

    """
    empty_name_list = []  # Список документов без указания имени

    print('В базе данных о документах есть информация о следующих владельцах:\n')
    for doc in documents:
        try:
            if doc['name'] == '':
                raise KeyError
            else:
                print(doc['name'])

        except KeyError:
            empty_name_list.append(doc['number'])

    print(' ')
    for empty_name_doc in empty_name_list:
        print(f'Для документа {empty_name_doc} не указан владелец')
    print(' ')


def main():
    print(instruct)
    while True:
        command = input('Введите команду: ').replace(' ', '')
        if command == 'p':
            people_by_number()
        elif command == 'l':
            all_doc_list()
        elif command == 's':
            doc_shell_find()
        elif command == 'a':
            add_new_doc()
        elif command == 'd':
            del_doc()
        elif command == 'm':
            doc_move()
        elif command == 'as':
            make_new_shelf()
        elif command == 'ado':
            all_doc_owners()
        elif command == 'q':
            print('Конец сеанса \n')
            break
        else:
            print('Такой команды нет в списке команд\n')

if __name__ == '__main__':

    main()
