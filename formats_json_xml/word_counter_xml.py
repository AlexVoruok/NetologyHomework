import xml.etree.ElementTree as ET

tree = ET.parse('newsafr.xml')
root = tree.getroot()

def n_char_words_from_xml_sorted_list_maker(xmlroot, char_n):
    ''' Принимает на вход корневой элемент xml дерева и число букв
        Возвращает отсортированный список кортежей, которые содержат в себе слово
        и количество его употреблений в текстах новостей.
        Список отсортирован по убыванию количества употреблений

    '''
    news_list = xmlroot.findall('channel/item')

    six_char_words = {}

    for news in news_list:
        for word in news[2].text.split(' '):
            if len(word) > char_n:
                if word not in six_char_words.keys():
                    six_char_words[word] = 1
                else:
                    six_char_words[word] += 1

    sorted_six_char_words = sorted(six_char_words.items(), key=lambda items: items[1], reverse=True)
    return sorted_six_char_words

letters_number = 6  # Можем задать количество букв. Будут искаться слова длиннее

sorted_words = n_char_words_from_xml_sorted_list_maker(root, letters_number)

print(f'Топ 10 самых часто встречающихся слов, длиной более {letters_number} букв: \n')

for topword in sorted_words[0:11]:
    print(f"   Слово '{topword[0]}' встречается {topword[1]} раз")