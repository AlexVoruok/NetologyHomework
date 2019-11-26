import json

try:
    with open('newsafr.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

except UnicodeDecodeError:
    print('Попробуйте другие варианты кодировки при чтении файла')

else:

    def list_of_news_maker_of_json(dict):
        ''' Функция принимает на вход словарь с заранее известной структурой
            Возвращает список всех слов новостей, переведённых в нижний регистр

        '''
        list_of_news = []

        for news in dict['rss']['channel']['items']:
            for word in news['description'].split(' '):
                list_of_news.append(word.lower())

        return list_of_news

    def n_words_counter(list, char_n):
        ''' Функция принимает на вход список слов и число
            Возвращает отсортированный список кортежей, которые содержат в себе слово
            и количество его употреблений в текстах новостей.
            Список отсортирован по убыванию количества употреблений

        '''
        n_char_words = {}
        for word in list:
            if len(word) > char_n:
                if word not in n_char_words.keys():
                    n_char_words[word] = 1
                else:
                    n_char_words[word] += 1

        sorted_n_char_words = sorted(n_char_words.items(), key=lambda items: items[1], reverse=True)
        return sorted_n_char_words

    def toplist(n_top, char_n, news_list):
        ''' :param n_top: количество позиций в топе
            :param char_n: количество букв, длиннее которого мы ищем слова
            :news_list: список слов из новостей
            :return: печатает топ упоминаний слов длиннее указанного количества

        '''

        sorted_words = n_words_counter(news_list, char_n)
        print(f'Топ {n_top} самых часто встречающихся слов, длиной более {char_n} букв: \n')

        for topword in sorted_words[0:n_top]:
            print(f"   Слово '{topword[0]}' встречается {topword[1]} раз")


    toplist(10, 6, list_of_news_maker_of_json(data))

