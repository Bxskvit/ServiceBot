from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram import F
from utils.computer_list_utils import get_postings, format_computers
from keyboards.kb_generator import create_inline_kb


# create a router
router: Router = Router()


@router.callback_query(F.data == "pc_list")
async def add_load(callback: CallbackQuery):
    # Example: postings is a list of dicts
    postings = await get_postings()
    formatted_posts = await format_computers(postings)

    # Build kwargs for create_inline_kb
    kwargs = {
        str(post["post_id"]): formatted_posts[i]  # key=callback_data, value=button text
        for i, post in enumerate(postings)
    }
    kb = create_inline_kb(width=1, **kwargs)

    back_kb = create_inline_kb(1, "go_back")

    kb.inline_keyboard.extend(back_kb.inline_keyboard)
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer(f"Here are available options.\n", reply_markup=kb, parse_mode='html')


