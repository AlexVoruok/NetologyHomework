class Animal:
    classname = 'животное'
    satiety = False  # Сытость
    voice = ' '

    def __init__(self, weight, name):
        self.weight = weight  # Задаём вес
        self.name = name  # Дайм имя

    def feed(self):
        self.satiety = True  # Покормим

    def make_voice(self):
        print(self.voice)


class Bird(Animal):
    classname = 'птица'
    eggs = 0  # средняя производительность, яиц/день

    def harwest(self):
        return self.eggs


class Goose(Bird):
    classname = 'гусь'
    voice = 'Га-Га'
    eggs = 1  # средняя производительность, яиц/день


class Duck(Bird):
    classname = 'утка'
    voice = 'Кря'
    eggs = 2  # средняя производительность, яиц/день


class Chicken(Bird):
    classname = 'курица'
    voice = 'Ко-ко-ко'
    eggs = 4  # средняя производительность, яиц/день


class MilkClovenFooted(Animal):
    classname = 'молочное парнокопытное'
    milk = 0  # литров в сутки

    def get_milk(self):
        return self.milk


class WoolClovenFooted(Animal):
    classname = 'шерстеносное парнокопытное'
    wool = 0  # кг шерсти в год

    def cut_wool(self):
        return self.wool


class Cow(MilkClovenFooted):
    classname = 'корова'
    voice = "Му"
    milk = 10  # литров в сутки


class Goat(MilkClovenFooted):
    classname = 'коза'
    voice = 'Ме'
    milk = 5  # литров в сутки


class Sheep(WoolClovenFooted):
    classname = 'овца'
    voice = "Бе"
    wool = 1  # кг шерсти в год


# создадим существующий набор животных
seriy = Goose(5, 'Серый')
beliy = Goose(4, 'Белый')
manka = Cow(200, 'Манька')
barashek = Sheep(50, 'Барашек')
kudryaviy = Sheep(60, 'Кудрявый')
koko = Chicken(1, 'Коко')
kukareku = Chicken(2, 'Кукареку')
roga = Goat(80, 'Рога')
kopita = Goat(100, 'Копыта')
krakva = Duck(2, "Кряква")

# Список данных нам животных
farm = [seriy, beliy, manka, barashek, kudryaviy, koko, kukareku, roga, kopita, krakva]


def get_harwest():
    """ собирает урожай за заданное количество дней

    """

    animal_to_harwest = input('\nУкажите через запятую, имя животных с кого надо собрать урожай: \n').replace(' ',
                                                                                                              '').split(
        ',')
    days_of_accum = int(input('\nУкажите сколько дней не собирали урожай \n'))

    print(f'\nЗа {days_of_accum} дня(ей):')
    if animal_to_harwest != ['']:  # Проверяем есть ли с кого собирать
        for animal in farm:  # Перебираем всех животных на ферме
            if animal.name in animal_to_harwest:  # ПРоверяем есть ли имя животного среди тех с кого надо собрать
                if isinstance(animal, Bird):  # В зависимости от класса животного собираем определённый продукт
                    print(f'{animal.classname} {animal.name} дал(а) {animal.eggs * days_of_accum}шт яиц\n')
                elif isinstance(animal, MilkClovenFooted):
                    print(f'{animal.classname} {animal.name} дал(а) {animal.milk * days_of_accum} литров молока\n')
                elif isinstance(animal, WoolClovenFooted):
                    print(f'{animal.classname} {animal.name} дал(а) {animal.wool * days_of_accum}кг шерсти\n')
    else:
        print('Ничего не собрано\n')


def get_weight():
    """ Взвешивает и выдаёт вес животных, суммарный вес и самое тяжелое животное

    """
    animal_to_weight = input('\nНапишите через запятую имена животных кого надо взвесить. \n'
                             'Или нажмите Enter, если надо взвесить всех:  \n').replace(' ', '').split(',')

    sorted_farm = sorted(farm, key=lambda x: x.weight, reverse=True)  # Отсортированный по весу список всех животных
    summed_weight = 0  # Счетчик суммируемого веса

    if animal_to_weight != ['']:  # УСловие для взвешивания животных введённых пользователем
        pass
    else:  # Взвешиваем всех
        animal_to_weight = [anim.name for anim in
                            sorted_farm]  # Создаём список имён из отсортированного по весу списка животных фермы

    for animal in sorted_farm:  # Перебираем всех животных в отсортированном по весу списке всех животных фермы
        if animal.name in animal_to_weight:  # Проверяем есть ли среди них те, кого нам надо взвесить
            print(f'{animal.classname} {animal.name} весит {animal.weight}кг ')
            summed_weight += animal.weight  # Суммируем вес
            if summed_weight == animal.weight:  # Определяем самое тяжёлое животное - это то, чей вес первым присуммируется в счётчик веса, т.к. все уже отсортированы по весу
                top_weight_animal = animal

    print(f'\nОбщий вес указанных животных составляет - {summed_weight}кг')
    print(
        f'Самое тяжёлое животное из них - {top_weight_animal.classname} {top_weight_animal.name} c весом {top_weight_animal.weight}кг')


def check_satiety():
    """ Проверяет состояние сытости

    """
    print('\nСостояние сытости поголовья: \n')
    for animal in farm:
        if animal.satiety:
            print(f'{animal.classname} {animal.name:10} - сыт и доволен')
        else:
            print(f'{animal.classname} {animal.name:10} - говорит {animal.voice} и просит есть')


def feed():
    """ Кормит животных

    """
    check_satiety()

    animal_to_feed = input('\nКого покормим?(назови имена): \n')
    print('\nХрум...Хрум..Хрум..\n')

    for animal in farm:
        if animal.name in animal_to_feed:
            animal.feed()

    check_satiety()


print('На ферме у дядюшки Джо живут: \n')
for animal in farm:
    print(f'{animal.classname} {animal.name}')

get_harwest()
get_weight()
feed()


