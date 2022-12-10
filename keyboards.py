from aiogram.types import ReplyKeyboardRemove, \
                          ReplyKeyboardMarkup, KeyboardButton, \
                          InlineKeyboardMarkup, InlineKeyboardButton


tattoo_master = InlineKeyboardButton('Тату мастер', callback_data='tattoo_master')
barber = InlineKeyboardButton('Барбер', callback_data='barber')

register = InlineKeyboardButton('Регистирация', callback_data = 'register')


role_kb = InlineKeyboardMarkup().add(tattoo_master, barber)
register_kb = InlineKeyboardMarkup().add(register)


role_arr = ['tattoo_master', 'barber']