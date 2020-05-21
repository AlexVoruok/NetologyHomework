import unittest
import random
from unittest.mock import patch, Mock
from VKinder.app.download_and_DB import save_to_db, client, check_and_get_ids
from VKinder.vkinder_main import VKUser
from VKinder.app.vkapi_client import get_user_data, search_people, get_profile_photo


class MainModuleTester(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.user_id = random.randint(1, 11111111)
        self.user_sex = random.randint(1, 2)
        self.search_count = random.randint(1, 1000)
        self.city_source = 'Екатеринбург'
        self.result_count = 10
        with patch('VKinder.vkinder_main.input', return_value=''):
            self.test_user = VKUser(self.user_id, base_user=True)

        list_of_photo_links = ['link1', 'link2', 'link3']
        test_pair = Mock(spec=VKUser)
        test_pair.top_three_photo = Mock(return_value=list_of_photo_links)
        test_pair.id = 123456
        self.test_list_of_vkusers = [test_pair, test_pair, test_pair, test_pair, test_pair]

    @classmethod
    def tearDownClass(self):
        # base = client[f'{self.test_user.id}']
        client.drop_database(f'{self.test_user.id}')

    def test_get_user_data(self):

        result = get_user_data(self.user_id)

        self.assertIsInstance(result, dict)
        self.assertIn('id', result)
        self.assertIn('first_name', result)
        self.assertIn('last_name', result)

    def test_search_people(self):

        result = search_people(self.user_sex, self.search_count, self.city_source)

        self.assertIsInstance(result, dict)
        self.assertIsInstance(result['items'], list)

    def test_get_profile_photo(self):
        phts = get_profile_photo(self.user_id)

        self.assertIn('items', list(phts.keys()))
        if phts.get('count', 0) > 0:
            self.assertIsInstance(phts['items'], list)

    def test_seek_for_pair_and_estimate(self):

        result = self.test_user.seek_for_pair_and_estimate(self.search_count, self.result_count)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], VKUser)

    def test_top_three_photo(self):
        result = self.test_user.top_three_photo()
        print(result)
        self.assertIsInstance(result, list)
        if result != ['Доступ к фотографиям пользователя ограничен']:
            for link in result:
                self.assertIn('http', link)

    def test_save_to_DB(self):

        save_to_db(self.test_user, self.test_list_of_vkusers)

        base = client[f'{self.test_user.id}']
        collections = base.list_collection_names()

        self.assertTrue(collections)

    def test_check_and_get_ids(self):
        result = check_and_get_ids(self.test_user)
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()
