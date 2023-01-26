from aiogram import executor
import logging

from src.config import dp

from time_task import on_sturtup, scheduler

from src.commands import commands_handler
from src.STATES.unregistered_user import register_handlers_telegram_start
from src.call_buttons import register_handlers_call_buttons
from src.STATES.admin_reg import register_handlers_admin_reg


logging.basicConfig(level=logging.INFO)


commands_handler(dp)
register_handlers_telegram_start(dp)
register_handlers_call_buttons(dp)
register_handlers_admin_reg(dp)


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup = on_sturtup)