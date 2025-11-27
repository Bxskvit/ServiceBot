from aiogram import types, Router
from aiogram.filters import Command
from keyboards.kb_generator import create_inline_kb
from aiogram.types import InlineKeyboardMarkup


# create a kb
kb: InlineKeyboardMarkup = create_inline_kb(2,"my_profile", "my_orders", "pc_list")

# create a router
router: Router = Router()


@router.message(Command(commands='start'))
async def bot_start_command(message: types.Message):
    await message.answer(f'HI, {message.from_user.first_name}', reply_markup=kb, parse_mode='html')