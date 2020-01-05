

class Contact:

    def __init__(self, name, family_name, phone, fav_contact=False, **additional):
        self.name = name
        self.family_name = family_name
        self.phone = phone
        self.fav_contact = fav_contact
        self.additional = additional

    def __str__(self):

        # Подготовка вывода информации про избранное
        if self.fav_contact:
            self.fav_switch = 'Да'
        else:
            self.fav_switch = 'Нет'

        # Подготовка вывода дополнительной информации
        self.additional_str = ''
        for field in self.additional.items():
            self.additional_str += f'\n    {field[0]} : {field[1]}'

        contact_data = f'Имя: {self.name} \n' \
                       f'Фамилия: {self.family_name} \n' \
                       f'Телефон: {self.phone} \n'\
                       f'В избранных: {self.fav_switch} \n'\
                       f'Дополнительная информация: {self.additional_str}'

        return contact_data


class PhoneBook:

    def __init__(self, bookname):
        self.bookname = bookname
        self.book = []

    def print_all_contacts(self):
        for contact in self.book:
            print(contact, '\n')

    def add_contact(self, name, family_name, phone, fav_contact=False, **additional):
        new = Contact(name, family_name, phone, fav_contact, **additional)
        self.book.append(new)

    def del_contact(self, number):
        """ Удаление контакта по номеру телефона

        """
        for contact in self.book:
            if contact.phone == number:
                self.book.remove(contact)
                print(f'Контакт {contact.name} {contact.family_name} удалён из книги \n')

    def print_favourites(self):
        """ Поиск всех избранных номеров

        """
        for contact in self.book:
            if contact.fav_contact:
                print(f'Контакт {contact.name} {contact.family_name} в Избранных \n')

    def find_contact(self, namepart):
        """ Поиск контакта по имени или фамилии
        Ввод допускается в любом порядке и регистре.
        Можно ввести как имя, так и имя с фамилией через пробел

        """
        parts_of_name = namepart.lower().split(' ')
        printed_list = []
        for contact in self.book:
            for part in parts_of_name:
                if part == contact.name.lower() or part == contact.family_name.lower():
                    if contact not in printed_list:  # проверяем не выводили ли мы данный контакт в этом запросе
                         printed_list.append(contact)
                         print(contact, '\n')

    def set_favorite(self, number):
        for contact in self.book:
            if contact.phone == number:
                contact.fav_contact = True
                print(f'Контакт {contact.name} {contact.family_name} добавлен в Избранные \n')



if __name__ == '__main__':
    testbook = PhoneBook('Alexbook')

    testbook.add_contact('Jhon', 'Smith', '+71234567809', telegram='@jhony', email='jhony@smith.com')
    testbook.add_contact('Jerry', 'Brown', '+7879879', telegram='@jmouse', email='jerry@smith.com')
    testbook.add_contact('Michael', 'Boon', '+7123123987', fav_contact=True, email='mboon@mail.com')


    testbook.print_all_contacts()
    testbook.print_favourites()
    testbook.set_favorite('+7879879')
    testbook.print_favourites()
    testbook.find_contact('smith brown')
    testbook.del_contact('+7879879')
    testbook.print_all_contacts()


