class UnpositiveIntError(Exception):
    def __init__(self):
        print('Вы ввели отрицательное число')

try:
    operator, operand1, operand2 = input('Введите арифметическое выражение с положительными'
                                         'числами в Польской нотации: ').split(' ')

    assert operator in ('+', '-', '*', '/')

    if int(operand1) < 0 or int(operand2) < 0:
        raise UnpositiveIntError

    if operator == '+':
         print('=', int(operand1) + int(operand2))
    elif operator == '-':
         print('=', int(operand1) - int(operand2))
    elif operator == '*':
         print('=', int(operand1) * int(operand2))
    elif operator == '/':
         print('=', int(operand1) / int(operand2))



except ValueError:
    print('Выражение вводится в формате: <знак операции>_<число1>_<число2>\n'
          'Попробуйте ещё раз')

except AssertionError:
    print('Недопустимая арифметическая операция')

except ZeroDivisionError:
    print('На ноль делить не допускается')

except UnpositiveIntError:
    print('\nВ домашке сказано - только положительные числа. \nДавайте снова.')

except Exception as ex:
    print(f'\nЧто-то пошло не так. \n{ex} \nПопробуйте ещё раз')


finally:
    print('\nВсем спасибо')

