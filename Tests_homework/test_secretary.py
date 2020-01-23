import unittest
from unittest.mock import patch
from Tests_homework.data_base import documents
from Tests_homework.data_base import directories
from Tests_homework import secretary_prog
from copy import deepcopy
import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def captured_output():
    old_out = sys.stdout
    try:
        sys.stdout = StringIO()
        yield sys.stdout
    finally:
        sys.stdout = old_out


class SecretaryProgTester(unittest.TestCase):

    def setUp(self):
        self.normal_doc_n = '11-2'
        self.normal_doc_name = "Геннадий Покемонов \n"
        self.doc_without_name = '1456 4568'
        self.normal_shelf = '1'
        self.shelf_to_moveon = '3'
        self.new_doc_number = '3333'
        self.new_doc_type = 'test doc'
        self.new_doc_name = 'Petr Tester'
        self.new_doc_wrong_shelf = '777'
        self.normal_shelf_list = '1, 2, 3'
        self.new_shelf = '5'

    # @unittest.skip(' ')
    def test_people_by_number(self):

        # тестируем три случая ввода - пустой ввод, полноценный номер документа, номер документа не имеющего
        # имени владельца. Эти параметры указаны в side_effect

        # Список образцов нормального вывода тестируемого метода
        normal_message_list = [secretary_prog.warning_doc_num,
                               self.normal_doc_name,
                               f'Для документа {self.doc_without_name} не указан владелец\n'
                               ]
        with patch('Tests_homework.secretary_prog.documents', deepcopy(documents)),\
             patch('Tests_homework.secretary_prog.directories', deepcopy(directories)):

            with patch('Tests_homework.secretary_prog.input', side_effect=['',
                                                                           self.normal_doc_n,
                                                                           self.doc_without_name]):
                for normal_message in normal_message_list:
                    with captured_output() as out:
                        self.assertEqual(secretary_prog.people_by_number(), None)

                    message = out.getvalue()
                    self.assertEqual(message, f'{normal_message}\n')

    # @unittest.skip(' ')
    def test_all_doc_list(self):

        with patch('Tests_homework.secretary_prog.documents', deepcopy(documents)), \
             patch('Tests_homework.secretary_prog.directories', deepcopy(directories)):

            with captured_output() as out:
                self.assertEqual(secretary_prog.all_doc_list(), None)

            self.assertEqual(type(out.getvalue()), str)
            self.assertEqual(len(out.getvalue().splitlines()), len(secretary_prog.documents))

    # @unittest.skip(' ')
    def test_doc_shelf_find(self):
        normal_message_list = [secretary_prog.warning_doc_num,
                               f'Этот документ лежит на полке {self.normal_shelf}'
                               ]

        with patch('Tests_homework.secretary_prog.documents', deepcopy(documents)), \
             patch('Tests_homework.secretary_prog.directories', deepcopy(directories)):

            with patch('Tests_homework.secretary_prog.input', side_effect=['', self.normal_doc_n]):
                for normal_message in normal_message_list:
                    with captured_output() as out:
                        self.assertEqual(secretary_prog.doc_shell_find(), None)

                    message = out.getvalue()
                    self.assertEqual(message, f'{normal_message}\n')

    # @unittest.skip('')
    def test_add_new_doc(self):

        with patch('Tests_homework.secretary_prog.documents', deepcopy(documents)), \
             patch('Tests_homework.secretary_prog.directories', deepcopy(directories)):

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
                self.assertEqual(message, f'{secretary_prog.warning_shelf} ' 
                                          f'\nСейчас есть полки с номерами {self.normal_shelf_list}\n')
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
                self.assertEqual(message, f'\nДокумент с номером {self.new_doc_number}' 
                                   f' добавлен на полку {self.normal_shelf} \n\n')
                self.assertGreater(after, before)

    def test_del_doc(self):

        with patch('Tests_homework.secretary_prog.documents', deepcopy(documents)), \
             patch('Tests_homework.secretary_prog.directories', deepcopy(directories)):

            # Тестируем попытку успешного удаления
            with patch('Tests_homework.secretary_prog.input', side_effect=[self.normal_doc_n]):

                before = len(secretary_prog.documents)

                with captured_output() as out:
                    self.assertEqual(secretary_prog.del_doc(), None)

                after = len(secretary_prog.documents)

                message = out.getvalue()
                self.assertEqual(message, f'Документ c номером {self.normal_doc_n} удалён из базы. \n\n')
                self.assertGreater(before, after)

            # Тестируем неудачную попытку удаления
            with patch('Tests_homework.secretary_prog.input', side_effect=[self.new_doc_number]):
                before = len(secretary_prog.documents)

                with captured_output() as out:
                    self.assertEqual(secretary_prog.del_doc(), None)

                after = len(secretary_prog.documents)

                message = out.getvalue()
                self.assertEqual(message, f'{secretary_prog.warning_doc_num}\n')
                self.assertEqual(before, after)

    def test_doc_move(self):

        with patch('Tests_homework.secretary_prog.documents', deepcopy(documents)), \
             patch('Tests_homework.secretary_prog.directories', deepcopy(directories)):

            with patch('Tests_homework.secretary_prog.input', side_effect = [self.normal_doc_n, self.shelf_to_moveon]):

                shelf_len_before = len(secretary_prog.directories[self.shelf_to_moveon])

                with captured_output() as out:
                    self.assertEqual(secretary_prog.doc_move(), None)

                shelf_len_after = len(secretary_prog.directories[self.shelf_to_moveon])

                message = out.getvalue()
                self.assertEqual(message, f'документ "{self.normal_doc_n}" перемещён на полку '
                                          f'{self.shelf_to_moveon} \n\n')
                self.assertGreater(shelf_len_after, shelf_len_before)

    def test_make_new_shelf(self):

        with patch('Tests_homework.secretary_prog.documents', deepcopy(documents)), \
             patch('Tests_homework.secretary_prog.directories', deepcopy(directories)):

            with patch('Tests_homework.secretary_prog.input', side_effect = [self.new_shelf]):

                shelfs_before = len(secretary_prog.directories)

                with captured_output() as out:
                    self.assertEqual(secretary_prog.make_new_shelf(), None)

                shelfs_after = len(secretary_prog.directories)

                message = out.getvalue()
                self.assertGreater(shelfs_after, shelfs_before)
                self.assertEqual(message, f'Новая полка с номером {self.new_shelf} создана \n\n')

    def test_all_doc_owners(self):

        with patch('Tests_homework.secretary_prog.documents', deepcopy(documents)), \
             patch('Tests_homework.secretary_prog.directories', deepcopy(directories)):

            with captured_output() as out:
                self.assertEqual(secretary_prog.all_doc_owners(), None)

            message = out.getvalue()
            self.assertEqual(message, 'В базе данных о документах есть информация о следующих владельцах:\n\n'
                                      'Василий Гупкин\n'
                                      'Геннадий Покемонов\n'
                                      'Аристарх Павлов\n \n'
                                      'Для документа 332 не указан владелец\n'
                                      'Для документа 1456 4568 не указан владелец\n \n')


if __name__ == '__main__':
    unittest.main()
