from aiogram import executor
import logging

from config import dp

from commands import commands_handler
from STATES.unregistered_user import register_handlers_telegram_start


logging.basicConfig(level=logging.INFO)


commands_handler(dp)
register_handlers_telegram_start(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)