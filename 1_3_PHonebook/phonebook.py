"""
1. Создать приложение "Телефонная книга". класс Contact имеет следующие поля:
Имя, фамилия, телефонный номер - обязательные поля;
Избранный контакт - необязательное поле. По умолчанию False;
Дополнительная информация(email, список дополнительных номеров, ссылки на соцсети) - необходимо использовать *args, **kwargs.
Переопределить "магический" метод str для красивого вывода контакта. Вывод контакта должен быть следующим

    jhon = Contact('Jhon', 'Smith', '+71234567809', telegram='@jhony', email='jhony@smith.com')
    print(jhon)

Вывод:

Имя: Jhon
Фамилия: Smith
Телефон: +71234567809
В избранных: нет
Дополнительная информация:
	 telegram : @jhony
	 email : jhony@smith.com

2. класс PhoneBook:
Название телефонной книги - обязательное поле;
Телефонная книга должна работать с классами Contact.
Методы:

Вывод контактов из телефонной книги;
Добавление нового контакта;
Удаление контакта по номеру телефона;
Поиск всех избранных номеров;
Поиск контакта по имени и фамилии.

*3. Продвинутый print (необязательное задание) Разработать свою реализацию функции print - adv_print. Она ничем не должна отличаться от классической функции кроме трех новых необязательных аргументов:

start - с чего начинается вывод. По умолчанию пустая строка;
max_line - максимальная длин строки при выводе. Если строка превышает max_line, то вывод автоматически переносится на новую строку;
in_file - аргумент, определяющ
"""


class Contact:

    def __init__(self, name, family_name, phone, fav_contact=False, **additional):
        self.name = name
        self.family_name = family_name
        self.phone = phone
        self.fav_contact = fav_contact
        self.additional = additional

    def __str__(self):

        self.favor_contacts = ''
        # Подготовка вывода данных о любимых контактах
        if self.fav_contact:
            for contact in self.fav_contact:
                self.favor_contacts += contact.name + ' ' + contact.family_name + ', '

        else:
            self.fav_contact = 'Нет'

        # Подготовка вывода дополнительной информации
        self.additional_str = ''
        for field in self.additional.items():
            self.additional_str += f'\n    {field[0]} : {field[1]}'

        contact_data = f'Имя: {self.name} \n' \
                       f'Фамилия: {self.family_name} \n' \
                       f'Телефон: {self.phone} \n'\
                       f'В избранных: {self.favor_contacts} \n'\
                       f'Дополнительная информация: {self.additional_str}'

        return contact_data


if __name__ == '__main__':
    jhon = Contact('Jhon', 'Smith', '+71234567809', telegram='@jhony', email='jhony@smith.com')
    jerry = Contact('Jerry', 'Brown', '+7879879', telegram='@jmouse', email='jerry@smith.com')
    mike = Contact('Michael', 'Boon', '+7123123987', fav_contact=(jhon, jerry), email='mboon@mail.com')
    print(jhon)
    print(' ')
    print(mike)
