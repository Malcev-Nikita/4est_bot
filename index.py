from aiogram import executor
import logging

from src.config import dp

from src.commands import commands_handler
from src.STATES.unregistered_user import register_handlers_telegram_start
from src.call_buttons import register_handlers_call_buttons


logging.basicConfig(level=logging.INFO)


commands_handler(dp)
register_handlers_telegram_start(dp)
register_handlers_call_buttons(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)