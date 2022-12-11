from aiogram.types import ReplyKeyboardRemove, \
                          ReplyKeyboardMarkup, KeyboardButton, \
                          InlineKeyboardMarkup, InlineKeyboardButton


## Кнопки
tattoo_master = InlineKeyboardButton('Тату мастер', callback_data='tattoo_master')
barber = InlineKeyboardButton('Барбер', callback_data='barber')

register = InlineKeyboardButton('Регистирация', callback_data = 'register')

menu = InlineKeyboardButton('Главное меню', callback_data = 'menu')
new_tasks = InlineKeyboardButton('Создать новую задачу', callback_data = 'new_tasks')

tasks_today = InlineKeyboardButton('Задачи на сегодня', callback_data = 'tasks_today')

## Клавиатуры
role_kb = InlineKeyboardMarkup().add(tattoo_master, barber)
register_kb = InlineKeyboardMarkup().add(register)
admin_kb = InlineKeyboardMarkup().add(menu, new_tasks)
menu = InlineKeyboardMarkup().add(tasks_today)


role_arr = ['tattoo_master', 'barber']