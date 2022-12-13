from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

## Кнопки
tattoo_master = InlineKeyboardButton('Тату мастер', callback_data='tattoo_master')
barber = InlineKeyboardButton('Барбер', callback_data='barber')

register = InlineKeyboardButton('Регистирация', callback_data = 'register')

menu = InlineKeyboardButton('Главное меню', callback_data = 'menu')
new_task = InlineKeyboardButton('Создать новую задачу', callback_data = 'new_task')

tasks_today = InlineKeyboardButton('Задачи на сегодня', callback_data = 'tasks_today')

confirm = InlineKeyboardButton('Подтвердить', callback_data = 'confirm')
reject = InlineKeyboardButton('Отклонить', callback_data = 'reject')

## Клавиатуры
role_kb = InlineKeyboardMarkup().add(tattoo_master, barber)
register_kb = InlineKeyboardMarkup().add(register)
admin_kb = InlineKeyboardMarkup().add(menu, new_task)
menu_kb = InlineKeyboardMarkup().add(tasks_today)
confirmation_kb = InlineKeyboardMarkup().add(confirm, reject)

def users_kb(users: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width = 3)

    for user in users:
        markup.insert(InlineKeyboardButton(f"{user}", callback_data=f"{user}"))
    return markup

role_arr = ['tattoo_master', 'barber']
confirmation_arr = ['confirm', 'reject']