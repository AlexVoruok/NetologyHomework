import unittest
from unittest.mock import patch
from Tests_homework.yandex_translator import our_translator
import json


class TestForYandexTranslator(unittest.TestCase):

    def setUp(self):
        self.api_key = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
        self.url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        self.wrong_api_key = 'SomWrongSetOfLetters'
        self.wrong_url = 'https://translate.yandex.net/api/badplace'

    def test_normal_translation(self):

        with patch('Tests_homework.yandex_translator.input', side_effect=['hi']):
            response = our_translator(self.api_key, self.url)

            self.assertEqual(response['code'], 200)
            self.assertEqual(response['text'][0], 'привет')

    # @unittest.skip('')
    def test_emty_input(self):

        with patch('Tests_homework.yandex_translator.input', side_effect=['']):
            response = our_translator(self.api_key, self.url)

            self.assertEqual(response['code'], 502)
            self.assertEqual(response['message'], 'Invalid parameter: text')

    # @unittest.skip('')
    def test_wrong_apikey(self):

        with patch('Tests_homework.yandex_translator.input', side_effect=['hi']):
            response = our_translator(self.wrong_api_key, self.url)

            self.assertEqual(response['code'], 401)
            self.assertEqual(response['message'], 'API key is invalid')

    # @unittest.skip('')
    def test_wrong_url(self):
        with patch('Tests_homework.yandex_translator.input', side_effect=['hi']):
            self.assertRaises(json.decoder.JSONDecodeError, our_translator, self.api_key, self.wrong_url)


if __name__ == '__main__':
    unittest.main()
