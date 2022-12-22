from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types


TOKEN = "5986825673:AAEVQNsig6A-QsMjZj_piIQ_n60M3Mc8yh0"

STORAGE = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode = types.ParseMode.HTML)
dp = Dispatcher(bot, storage=STORAGE)

HOST = 'localhost'
USER = 'root'
PASSWD = ''
DB = '4est_duty_bot'