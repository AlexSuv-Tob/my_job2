#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью спе циальных карточек, на которых отмечены числа,
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр,
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается
случайная карточка.

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.

Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71
--------------------------
-- Карточка компьютера ---
 7 87     - 14    11
      16 49    55 88    77
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать
модуль random: http://docs.python.org/3/library/random.html

"""
import random


class LotoGame:

    def __init__(self, player, computer):
        self._player = player
        self._computer = computer
        # Тут с помощью random.sample я получаю не повторяющиеся числа
        self._NUMBERS_COUNT = 90
        MAX_NUMBER = 90
        # Вы можете использовать random.shuffle на сгенерированном списке, например генератором списков!
        self._numbers_in_bag = random.sample(range(1, MAX_NUMBER + 1), self._NUMBERS_COUNT)

    def _get_number(self):
        return self._numbers_in_bag.pop()

    def start(self):
        for i in range(self._NUMBERS_COUNT):
            print(self._player, self._computer)
            number = self._get_number()
            print('Новый бочонок {}, осталось {}'.format(number, len(self._numbers_in_bag)))
            choice = input('Хотите зачеркуть? y/n:\n')
            if choice == 'y':
                # Тут мы зачеркиваем число если оно есть, если нет, а игрок попытался, то он проиграл.
                if not self._player.try_stroke_number(number):
                    print('Игрок проиграл!')
                    break
            elif self._player.has_number(number):
                print('Игрок проиграл!')
                break
            # Компьютер не ошибается =)
            # if random.random() < 0.02:
            #     pass  # в 2% случаеав
            if self._computer.has_number(number):
                self._computer.try_stroke_number(number)


class LotoCard:

    def __init__(self, player_type):
        self.player_type = player_type
        self._card = [[],
                      [],
                      []]
        self._MAX_NUMBER = 90
        self._MAX_NUMBERS_IN_CARD = 15
        self._numbers_stroked = 0
        NEED_SPACES = 4
        NEED_NUMBERS = 5

        # Числа для будущей карты лото
        # random.sample - позволяет получить набор случайных, но уникальных чисел!
        self._numbers = random.sample(range(1, self._MAX_NUMBER + 1), self._MAX_NUMBERS_IN_CARD)

        # цикл вставляющий пробелы и цифры в нашу карту
        for line in self._card:
            for _ in range(NEED_SPACES):
                line.append(' ')
            for _ in range(NEED_NUMBERS):
                line.append(self._numbers.pop())

        # Данная функция возвращает либо число, которое непосредственно на линии, либо случайное, чтобы случайно расставить пробелы.
        def check_sort_item(item):
            if isinstance(item, int):
                return item
            return random.randint(1, self._MAX_NUMBER)

# [' ',' ',' ',' ', 80,2,1,3,5]
# [' ', 80, 3,2,1, ' ']
# [1, ' ', 2, 3, ' ', 80]
#[3 25]

        # Здесь мы именно сортируем списки внутри списка
        for index, line in enumerate(self._card):
            self._card[index] = sorted(line, key=check_sort_item)


    def has_number(self, number):
        for line in self._card:
            if number in line:
                return True
        return False

    def try_stroke_number(self, number):
        for index, line in enumerate(self._card):
            for num_index, number_in_card in enumerate(line):
                if number == number_in_card:
                    self._card[index][num_index] = '-'
                    self._numbers_stroked += 1
                    if self._numbers_stroked >= self._MAX_NUMBERS_IN_CARD:
                        raise Exception('{} победил!'.format(self.player_type))
                    return True
        return False
# ['23 ', '11 ', '3  ', ' 56']
# [     1  3 56]
    # Метод для строкового представления объекта
    def __str__(self):
        MAX_FIELD_LENGTH = 3
        header = '\n{}:\n--------------------------'.format(self.player_type)
        body = '\n'
        for line in self._card:
            for field in line:
                body += str(field).ljust(MAX_FIELD_LENGTH)  # Выравниваем, добавляя пробелы, если это необходимо.
            body += '\n'
        return header + body

human_player = LotoCard('Игрок')
computer_player = LotoCard('Компьютер')

game = LotoGame(human_player, computer_player)
game.start()
