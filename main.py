import datetime as dt

# ОБЩИЕ КОММЕНТАРИИ
# Неиспользованный импорт json -> следует убрать
# Отсутствуют межстрочные отступы - по 2 между объявлением класса, по одному
#     у методов класса
# Отсутствуют отступы в присваивании переменных, в операциях сложения/
#     вычитания/деления
# Отсутствуют docstrings в классах и методах классов (в методе класса
#     CaloriesCalculator get_calories_remained() использован однострочный
#     комментарий вместо docstring)
# Внутри методов в определенных местах желательны логические отступы (например
#     в методе get_today_cash_remainder() класса CashCalculator между двумя
#     if'ами)


class Record:
    def __init__(self, amount, comment, date=None):
        # в качестве значения по умолчанию аргумента `date` следует
        # использовать None, но не ''
        self.amount = amount
        # в объявлении self.date следует сделать многострочный `if`, чтобы
        # уложиться в 79-символьное ограничение И для читабельности кода
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.datetime.now().date()

        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0

        # в цикле не следует использовать переменнуюю с именем Record - точно
        # такое же название имеет класс `Record` (+ переменную следует
        # назвать с маленькой буквы)
        for rec in self.records:
            if rec.date == dt.datetime.now().date():
                today_stats += rec.amount

        return today_stats

    def get_week_stats(self):
        today = dt.datetime.now().date()
        week_stats = 0

        for record in self.records:
            # поскольку дельта `сегодня минус прошедший день` всегда больше
            # либо равна нуля, условие в цикле можно сократить, опустив
            # проверку (today - record.date).days >= 0:
            if (today - record.date).days < 7:
                week_stats += record.amount()

        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        # вместо комментария к функции следует использовать docstring

        # имя переменной `x` не несет смысловой нагрузки ->
        # заменим на `remainder`
        remainder = self.limit - self.get_today_stats()

        if remainder > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей' \
                   f' калорийностью не более {remainder} кКал'
        # поскольку в блоке `if` есть return, блок `else` можно опустить,
        # оставив просто return
        return 'Хватит есть!'


class CashCalculator(Calculator):
    # излишнее преобразование констант из int в float ->
    # достаточно объявить переменные сразу типа float
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        # метод принимает лишние аргумеенты USD_RATE и EURO_RATE ->
        # внутри этого метода следует обращатся к глобальным переменным
        # класса через `self`: например `self.USD_RATE`

        cash_remained = self.limit - self.get_today_stats()

        # `currency_type` можно вынести из условия `if` и определить через
        # словарь, сократив код и добавив гибкости к изменениям:
        curr_type = {'usd': 'USD', 'eur': 'EUR', 'rub': 'руб'}[currency]

        if currency == 'usd':
            cash_remained /= self.USD_RATE
        elif currency == 'eur':
            cash_remained /= self.EURO_RATE
        # здесь количество `elif` можно сократить, т.к. проверка
        # `elif currency_type == 'rub'` не нужна

        # округление `cash_remained` можно вынести перед `if`, чтобы
        # не повторяться в форматировании строк (не использовать
        # вычисления дважды в двух форматированиях):
        cash_remained = round(cash_remained, 2)

        if cash_remained > 0:
            return f'На сегодня осталось {cash_remained} {curr_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'

        # последний `elif cash_remind < 0:` также можно опустить, т.к.
        # перед ним просиходит return
        return 'Денег нет, держись: твой долг - {0} {1}'.format(
            -cash_remained, curr_type)

    # метод `get_week_stats()` можно убрать, т.к. он не несет изменений
    # от родительского класса
