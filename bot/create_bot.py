from aiogram import Bot, Dispatcher
from config import get_telegram_token

TELEGRAM_TOKEN = get_telegram_token()

bot = Bot(TELEGRAM_TOKEN)

dp: Dispatcher = Dispatcher()
