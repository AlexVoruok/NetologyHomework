import json

try:
    with open('newsafr.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

except UnicodeDecodeError:
    print('Попробуйте другие варианты кодировки при чтении файла')

else:

    def n_char_words_sorted_list_maker(dict, char_n):
        ''' Функция принимает на вход словарь с заранее известной структурой
            и число.
            Возвращает отсортированный список кортежей, которые содержат в себе слово
            и количество его употреблений в текстах новостей.
            Список отсортирован по убыванию количества употреблений

        '''

        six_char_words = {}

        for news in dict['rss']['channel']['items']:
            for word in news['description'].split(' '):
                if len(word) > char_n:
                    if word not in six_char_words.keys():
                        six_char_words[word] = 1
                    else:
                        six_char_words[word] += 1

        sorted_six_char_words = sorted(six_char_words.items(), key=lambda items: items[1], reverse=True)
        return sorted_six_char_words

    letters_number = 6   # Можем задать количество букв. Будут искаться слова длиннее

    sorted_words = n_char_words_sorted_list_maker(data, letters_number)

    print(f'Топ 10 самых часто встречающихся слов, длиной более {letters_number} букв: \n')

    for topword in sorted_words[0:11]:
        print(f"   Слово '{topword[0]}' встречается {topword[1]} раз")

