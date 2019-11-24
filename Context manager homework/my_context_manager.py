from contextlib import contextmanager
from datetime import datetime

@contextmanager
def my_manager(path):
    try:
        file = open(path, 'r+', encoding='utf8')
        yield file
    finally:
        file.close()

def reader_writer(stream):
    ''' Эта функция получает на вход дескриптор файла. Файл содержит несколько списков снаряжения
        с указанием веса.
        Функция суммирует вес для каждого из списков снаряжения и дописывает в конец файла эту информацию.
        Также в ней содрежится специальный пустой цикл для "затягивания" времени.

    '''

    list_of_weights = []  # Список куда последовательно будет заносится информация о весах каждого из списков снаряжения
    list_counter = 0  # Счётчик списков, чтобы правильно указать его номер

    while True:  # Цикл который проходится по разным спискам снаряжения
        for i in range(10000000):  # Затягватель времени
            pass
        list_counter += 1
        try:
            eqip_sum = 0  # Счётчик веса для списка снаряжения
            while True:  # Этот цикл проходится по отдельным элементам в списке снаряжения

                first_string = stream.readline()
                if '*' in first_string :  # Проверяем не закончился ли список снаряжения
                    break

                else:
                    eqip_sum += float(stream.readline())
                    stream.readline()

            list_of_weights.append(f'Вес {list_counter} списка снаряжения - {str(round(eqip_sum, 2))}кг')
        except ValueError:  # Это исключение происходит, когда после разделителя ***.. программа вместо следующего списка находит что-то кроме чисел в строке
            break


    stream.write('\n'.join(list_of_weights))


with my_manager('eqip_list.txt') as eqip_list:
    time_start = datetime.now()
    reader_writer(eqip_list)
    time_end = datetime.now()
    print('Время выполнения программы ч:мм:сс: ', time_end-time_start)
