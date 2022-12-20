from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from datetime import date
from calendar import monthrange


## Кнопки
tattoo_master = InlineKeyboardButton('Тату мастер', callback_data='tattoo_master')
barber = InlineKeyboardButton('Барбер', callback_data='barber')
administrator = InlineKeyboardButton('Администратор', callback_data='administrator')
preadmin = InlineKeyboardButton('Запрос на админа', callback_data='preadmin')

register = InlineKeyboardButton('Регистирация', callback_data = 'register')

menu = InlineKeyboardButton('Главное меню', callback_data = 'menu')
new_task = InlineKeyboardButton('Создать новую задачу', callback_data = 'new_task')

tasks_today = InlineKeyboardButton('Задачи на сегодня', callback_data = 'tasks_today')
new_task_me = InlineKeyboardButton('Создать себе задачу', callback_data = 'new_task_me')

confirm = InlineKeyboardButton('Подтвердить', callback_data = 'confirm')
reject = InlineKeyboardButton('Отклонить', callback_data = 'menu')

everyday_task = InlineKeyboardButton('Ежедневная задача', callback_data = 'everyday_task')
date_task = InlineKeyboardButton('Календарь', callback_data = 'date_task')

next = InlineKeyboardButton('>', callback_data = 'next')
back = InlineKeyboardButton('<', callback_data = 'back')

## Клавиатуры
role_kb = InlineKeyboardMarkup(row_width = 3).add(tattoo_master, barber, administrator, preadmin)
register_kb = InlineKeyboardMarkup().add(register)
admin_kb = InlineKeyboardMarkup().add(menu, new_task)
menu_kb = InlineKeyboardMarkup().add(tasks_today, new_task_me)
confirmation_kb = InlineKeyboardMarkup().add(confirm, reject)
task_type_kb = InlineKeyboardMarkup().add(everyday_task, date_task)

def users_kb(users: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width = 3)

    for user in users:
        markup.insert(InlineKeyboardButton(f"{user}", callback_data=f"{user}"))
    return markup


def calendar_kb(year: int, month: int) -> InlineKeyboardMarkup:
    calendar = InlineKeyboardMarkup(row_width = 7)
    days_of_the_week = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПЯ', 'СБ', 'ВС']
    month_ru = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    month_button = InlineKeyboardButton(f"{month_ru[month - 1]} - {year}", callback_data = f"{month_ru[month - 1]}")

    for day_of_the_week in days_of_the_week:
        calendar.insert(InlineKeyboardButton(f"{day_of_the_week}", callback_data = f"{day_of_the_week}"))

    days = monthrange(year, month)[1]
    start_day = datetime.weekday(date(year, month, 1))
    end_day = abs(((start_day + days) % 7) - 7)
    i = 1

    while start_day > 0:
        calendar.insert(InlineKeyboardButton(" ", callback_data = " "))
        start_day -= 1

    while i <= days:
        calendar.insert(InlineKeyboardButton(f"{i}", callback_data = f"{i}"))
        i += 1

    while end_day > 0:
        calendar.insert(InlineKeyboardButton(" ", callback_data = " "))
        end_day -= 1

    calendar.add(back, month_button, next)

    return calendar



role_arr = ['tattoo_master', 'barber', 'administrator', 'preadmin']
confirmation_arr = ['confirm', 'reject']
task_type_arr = ['everyday_task', 'date_task']
button_calendar_arr = ['next', 'back']