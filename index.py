from aiogram import executor
import logging

from src.config import dp

from src.commands import commands_handler
from src.STATES.unregistered_user import register_handlers_telegram_start
from src.STATES.new_task import register_handlers_new_tasks


logging.basicConfig(level=logging.INFO)


commands_handler(dp)
register_handlers_telegram_start(dp)
register_handlers_new_tasks(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)