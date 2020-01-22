import unittest
from unittest.mock import patch
from Tests_homework.data_base import documents
from Tests_homework.data_base import directories
from Tests_homework import secretary_prog
from copy import deepcopy
import sys
from contextlib import contextmanager
from io import StringIO


copy_documents = deepcopy(documents)
copy_directories = deepcopy(directories)


@contextmanager
def captured_output():
    old_out = sys.stdout
    try:
        sys.stdout = StringIO()
        yield sys.stdout
    finally:
        sys.stdout = old_out


@patch('Tests_homework.secretary_prog.documents', copy_documents)
@patch('Tests_homework.secretary_prog.directories', copy_directories)
class SecretaryProgTester(unittest.TestCase):

    def setUp(self):
        self.normal_doc_n = '11-2'
        self.normal_doc_name = "Геннадий Покемонов" + ' \n'
        self.doc_without_name = '1456 4568'
        self.normal_shelf = '1'
        self.new_doc_number = '3333'
        self.new_doc_type = 'test doc'
        self.new_doc_name = 'Petr Tester'
        self.new_doc_wrong_shelf = '777'
        self.normal_shelf_list = '1, 2, 3'
        self.normal_message_wrong_shelf = f'{secretary_prog.warning_shelf} ' \
                                          f'\nСейчас есть полки с номерами {self.normal_shelf_list}\n'
        self.success_add_doc_mes = f'\nДокумент с номером {self.new_doc_number}' \
                                   f' добавлен на полку {self.normal_shelf} \n\n'

    # @unittest.skip('вместе не работают')
    def test_people_by_number(self):

        # тестируем три случая ввода - пустой ввод, полноценный номер документа, номер документа не имеющего
        # имени владельца. Эти параметры указаны в side_effect

        # Список образцов нормального вывода тестируемого метода
        normal_message_list = [secretary_prog.warning_doc_num,
                               self.normal_doc_name,
                               f'Для документа {self.doc_without_name} не указан владелец\n'
                               ]

        with patch('Tests_homework.secretary_prog.input', side_effect=['', self.normal_doc_n, self.doc_without_name]):
            for normal_message in normal_message_list:
                with captured_output() as out:
                    self.assertEqual(secretary_prog.people_by_number(), None)

                message = out.getvalue()
                self.assertEqual(message, normal_message + '\n')

    # @unittest.skip('вместе не работают')
    def test_all_doc_list(self):
        print('test_all_doc_list')
        with captured_output() as out:
            self.assertEqual(secretary_prog.all_doc_list(), None)

        self.assertEqual(type(out.getvalue()), str)
        self.assertEqual(len(out.getvalue().splitlines()), len(secretary_prog.documents))

        # print(out.getvalue())

    @unittest.skip('вместе не работают')
    def test_doc_shelf_find(self):
        normal_message_list = [secretary_prog.warning_doc_num,
                               f'Этот документ лежит на полке {self.normal_shelf}'
                               ]

        with patch('Tests_homework.secretary_prog.input', side_effect=['', self.normal_doc_n]):
            for normal_message in normal_message_list:
                with captured_output() as out:
                    self.assertEqual(secretary_prog.doc_shell_find(), None)

                message = out.getvalue()
                self.assertEqual(message, normal_message + '\n')

    @unittest.skip('вместе не работают')
    def test_add_new_doc(self):

        print('test_add_new_doc')

        # Тест попытки добавления с ошибочной полкой - провал попытки
        with patch('Tests_homework.secretary_prog.input', side_effect=[self.new_doc_number,
                                                                       self.new_doc_type,
                                                                       self.new_doc_name,
                                                                       self.new_doc_wrong_shelf
                                                                       ]):

            before = len(secretary_prog.documents)

            with captured_output() as out:
                self.assertEqual(secretary_prog.add_new_doc(), None)

            after = len(secretary_prog.documents)

            message = out.getvalue()
            self.assertEqual(message, self.normal_message_wrong_shelf)
            self.assertEqual(after, before)

        # Тест удачной попытки добавления
        with patch('Tests_homework.secretary_prog.input', side_effect=[self.new_doc_number,
                                                                       self.new_doc_type,
                                                                       self.new_doc_name,
                                                                       self.normal_shelf
                                                                       ]):
            before = len(secretary_prog.documents)
            with captured_output() as out:
                self.assertEqual(secretary_prog.add_new_doc(), None)

            after = len(secretary_prog.documents)

            message = out.getvalue()
            self.assertEqual(message, self.success_add_doc_mes)
            self.assertGreater(after, before)

    def test_del_doc(self):
        pass

    def test_doc_move(self):
        pass

    def test_make_new_shelf(self):
        pass

    def test_all_doc_owners(self):
        pass


if __name__ == '__main__':
    unittest.main()
