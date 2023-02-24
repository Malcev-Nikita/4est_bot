from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types



TOKEN         = "6167962615:AAE89WBo_c3ewtw0n2hpHrs8UA9QbYaa2Wg" # Тест
# TOKEN         = "5986825673:AAEVQNsig6A-QsMjZj_piIQ_n60M3Mc8yh0" # Не тест

STORAGE       = MemoryStorage()

bot           = Bot(token=TOKEN, parse_mode = types.ParseMode.HTML)
dp            = Dispatcher(bot, storage=STORAGE)

HOST          = '92.53.105.154'
USER          = 'gen_user'
PASSWD        = '3w2S6xi3fTVZnRR'
DB            = 'default_db'

code_admin    = 'Честь'