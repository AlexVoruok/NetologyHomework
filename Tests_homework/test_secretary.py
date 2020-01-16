import unittest
import json
from unittest.mock import Mock
from unittest.mock import patch
from Tests_homework.data_base import documents
from Tests_homework.data_base import directories
from Tests_homework import secretary_prog
from copy import copy


copy_documents = copy(documents)
copy_directories = copy(directories)

@patch('secretary_prog.documents', 'замена для документс')
@patch('secretary_prog.directories', copy_directories)
class secretary_prog_tester(unittest.TestCase):

    def setUp(self):
        pass

    def test_people_by_number(self):
        with patch('secretary_prog.input', return_value = '11-2' ):
            print(secretary_prog.documents)
            secretary_prog.people_by_number()

    def test_all_doc_list(self):
        pass

    def test_doc_shelf_find(self):
        pass

    def test_add_new_doc(self):
        pass

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
