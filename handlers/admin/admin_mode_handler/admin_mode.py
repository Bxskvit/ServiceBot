from aiogram import types, Router
from aiogram.filters import Command
from keyboards.kb_generator import create_inline_kb
from aiogram.types import InlineKeyboardMarkup
from filters.custom_filters import AccessLevelFilter

# create a kb
# kb: InlineKeyboardMarkup = create_inline_kb(...)

# create a router
router: Router = Router()


@router.message(Command(commands='admin'), AccessLevelFilter(1))
async def bot_start_command(message: types.Message):
    await message.answer(f'Admin mode {message.from_user.first_name}', parse_mode='html')
