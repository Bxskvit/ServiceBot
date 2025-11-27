from aiogram import Router
from aiogram.types import CallbackQuery
from filters.custom_filters import PostIDFilter

router = Router()


@router.callback_query(PostIDFilter())  # dynamically checks if callback is a valid post ID
async def handle_post_id(callback: CallbackQuery):
    post_id = int(callback.data)  # convert callback data to integer
    await callback.answer(f"You clicked on post ID: {post_id}")
