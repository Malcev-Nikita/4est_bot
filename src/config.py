from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types



# TOKEN         = "6167962615:AAE89WBo_c3ewtw0n2hpHrs8UA9QbYaa2Wg"
# TOKEN         = "5986825673:AAEVQNsig6A-QsMjZj_piIQ_n60M3Mc8yh0"
STORAGE       = MemoryStorage()

bot           = Bot(token=TOKEN, parse_mode = types.ParseMode.HTML)
dp            = Dispatcher(bot, storage=STORAGE)

HOST          = '92.53.105.154'
USER          = 'gen_user'
PASSWD        = '3w2S6xi3fTVZnRR'
DB            = 'default_db'

tattoo_master = [ 'Найди 4 подборки с эскизами в интернете или pinterest, для акции в сторис',
                  'Скинь администратору подборки с акционными эскизам из интернета',
                  'Загрузи акционные эскизы из интернета себе в сторис, в инсту и вк',
                  'Выложи сторис себе в вотсап',
                  'Нарисуй 1 простой эскиз, для своего поста в аккаунт Честь',
                  'Придумай идею для эскиза на рисовашки на среду',
                  'Сделай рассылку в инсте и вк разным незнакомым людям (20 сообщений) (Привет я "ИМЯ", и я делаю классыные татуировки по приятной цене) Ты хочешь себе что-нибудь набить? Давай я тебя проконсультирую)',
                  'Напиши своим старым клиентам (Привет, как дела? Может сделаем тебе новую татуировку?)',
                  'Залей сторис, перевод трансфера, к себе в сторис, в инсту и вк (Попроси админа снять на твой телефон)',
                  'Залей сториc, процесс татуирования, себе в инсту и вк (Попроси админа снять на твой телефон)',
                  'Залей сторис, итога татуировки, себе в инсту и вк (Попроси админа снять на твой телефон)',
                  'Сделай фото с клиентом',
                  'Залей фото с клиентом, себе в инсту и вк',
                  'Скинь фото с клиентом админу',
                  'Попроси клиента выложить у себя сторис с отметкой Честь клуба',
                  'Попроси клиента оставить отзыв 2gis, Google, Яндекс (Где удобно)' ]

tattoo_master_everyday = [ 'Фото с собой и приветствие (вк, инст, вотс)',
                           'Акция (эскиз, пинтерест и т.д.) без слова акция и скидка (вк, инст, вотс)',
                           'Твоё тату (фото, видео) (вк, инст, вотс)',
                           'Рассылка Инст - 20шт, Вк - 15шт',
                           'Пост со своей тату (вк, инст, вотс)' ]

administrator = [ 'Вытащить штендер на улицу',
                  'Уборка (Протереть пыль на холодильнике, полках, обувнице, диване и т.д. Помыть пол в тату зоне и в зоне дивана)',
                  'Протереть красные тапочки от пыли',
                  'Выкинуть мусор из всех вёдер (бахилы, кулер, туалет, зона X, стерилка) + засунуть в вёдра новые пакеты',
                  'Сторис с акционными эскизами от мастера, в инст и вк',
                  'Выложи сторис в вотсап чести',
                  'Ответить на сообщения (инст, вк, whatsApp, авито, amoCRM)',
                  'Проверить сообщения на авито',
                  'Проверить комментарии под постами, в инст и вк (ответить и предложить набить татуировку)',
                  'Ответить в amoCRM по задачам (дни рождени, как заживление, может есть идеи для новой тату)',
                  'Рассылка в инст и вк (по 20 сообщений) (Добрый день, вы хотите себе татуировку? Мы профессиональная тату студия "Честь". Делаем качественные татуировки по приятным ценам. Давайте вас бесплатно проконсультируем)',
                  'Напомнить мастерам сфоткаться с клиентом',
                  'Проверить рассходники, то что кончилось заказать (вода, скотч, бритвы, простыни, пелёнки, туалетная бумага, пакеты)',
                  'Проверить и если кончилось купить (чай, молоко, кофе, сахар)',
                  'Проверить цветы (поливаем раз в неделю)',
                  'Заполнить отчёт (прибыль, кол.во клиентов, магазин)',
                  'Заполнить отчёт "Клиенты откуда',
                  'Напечатать чек на кассовом аппарате на 2.000 руб',
                  'Написать отчет о заявках в вотсап аккаунт - ЧЕСТЬ записи',
                  'Выключить сплитуху',
                  'Занести штендер',
                  'Закрыть все двери',
                  'Сторис, акция, эскизы от мастера (инста и вк)',
                  'Сторис, тату обучение (инста и вк)',
                  'Сторис, имидж (инста и вк)',
                  'Сторис, тату в кредит (иснта и вк)',
                  'Сторис, тату сертификата (иснта и вк)',
                  'Сторис, перевод рисунка (инста и вк)',
                  'Сторис, процесс татуирования (инста и вк)',
                  'Сторис, итог татуировки (инста и вк)',
                  'Сторис с клиентом (инста и вк)',
                  'Предложить клиенту чай или кофе',
                  'Узнать у клиенат всё ли ему понравилось',
                  'Узнать у клиента день рождение и добавить в amoCRM',
                  'Попроси клиента заполнить опросник',
                  'Поблагодарить клиента (Спасибо что выбрали нас, приходите к нам ещё, будем вам рады)',
                  'Добавить контакты с опросника на рабочий телефон и амо срм',
                  'Поставить напоминалку в amoCRM (через две недели узнать про заживление)',
                  'Отправить благодарственное сообщение клиентам после сеанса. (текс сообщения в заметках рабочего телефона)' ]

code_admin    = 'Честь'