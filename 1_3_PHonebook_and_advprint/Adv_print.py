def adv_print(*args, start='', max_line=0, in_file=''):
    """ Ничем не отличаться от классической функции кроме трех новых необязательных аргументов:

    start - с чего начинается вывод. По умолчанию пустая строка;
    max_line - максимальная длин строки при выводе. Если строка превышает max_line,
    то вывод автоматически переносится на новую строку;
    in_file - аргумент, определяющий будет ли записан вывод ещё и в файл.

    """

    to_export = ''  # В этой переменной накапливается единая строка для вывода из всего набора *args
    to_print = ''  # Этой переменной присваивается строка для вывода с учётом max_line
    to_export += start  # Учтём параметр start

    # Сделаем единую строку для вывода из всего набора *args
    for arg in args:
        to_export += str(arg)

    # Если параметр max_line введён, сделаем строку для вывода с учётом него
    if round(max_line):
        i = 0
        for char in to_export:
            i += 1
            to_print += char
            if i % round(max_line) == 0:
                to_print += '\n'
    else:
        to_print = to_export

    # Запись дополнительно в файл если in_file == True
    if in_file:
        with open(in_file, 'w', encoding='utf-8') as file:
            file.write(to_print)
    else:
        print('не в файл')

    return print(to_print)


if __name__ == '__main__':

    text = 'Продвинутый print (необязательное задание) Разработать свою реализацию функции ' \
           'print - adv_print. Она ничем не должна отличаться от классической функции кроме трех ' \
           'новых необязательных аргументов:'

    tuple = (4, 5, 6)
    adv_print(1, 2, 3, tuple, text, max_line=50, in_file='output.txt')
