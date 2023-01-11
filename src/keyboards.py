from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


## Кнопки
tattoo_master = InlineKeyboardButton('Тату мастер', callback_data='tattoo_master')
administrator = InlineKeyboardButton('Администратор', callback_data='administrator')
admin = InlineKeyboardButton('Хозяин', callback_data='admin')

register = InlineKeyboardButton('Регистирация', callback_data = 'register')

tasks_today = InlineKeyboardButton('Задачи на сегодня', callback_data = 'tasks_today')

confirm = InlineKeyboardButton('✅', callback_data = "confirm")

complete = InlineKeyboardButton('Ты красава, задача выполнена, поехали дальше', callback_data = 'complete')

## Клавиатуры
role_kb = InlineKeyboardMarkup(row_width = 3).add(tattoo_master, administrator, admin)
register_kb = InlineKeyboardMarkup().add(register)
menu_kb = InlineKeyboardMarkup().add(tasks_today)
task_kb = InlineKeyboardMarkup().add(confirm)
complete_kb = InlineKeyboardMarkup().add(complete)

def users_kb(users: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width = 3)

    for user in users:
        markup.insert(InlineKeyboardButton(f"{user}", callback_data=f"{user}"))
    return markup


role_arr = ['tattoo_master', 'administrator', 'admin']