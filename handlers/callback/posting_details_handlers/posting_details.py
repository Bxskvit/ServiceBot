from aiogram import Router
from aiogram.types import CallbackQuery
from filters.custom_filters import PostIDFilter
from utils.database_utils import AsyncComputersRepository
from utils.computer_list_utils import format_computer_description_message
from keyboards.kb_generator import create_inline_kb

router = Router()

kb = create_inline_kb(2, "go_back", "bid")


@router.callback_query(PostIDFilter())  # dynamically checks if callback is a valid post ID
async def handle_post_id(callback: CallbackQuery):
    post_id = int(callback.data)  # convert callback data to integer
    computers_list = AsyncComputersRepository()
    computer = await computers_list.get_computer(post_id=post_id)

    description = format_computer_description_message(computer=computer)

    await callback.message.delete()
    await callback.answer(f"You clicked on post ID:{computer[0]}")
    await callback.message.answer(f"{description}", reply_markup=kb, parse_mode='html')
