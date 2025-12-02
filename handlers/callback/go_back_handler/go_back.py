from aiogram.types import InlineKeyboardMarkup
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

# create a router
router: Router = Router()


@router.callback_query(lambda c: c.data == "go_back")
async def go_back(callback, state: FSMContext):
    data = await state.get_data()
    stack = data.get("screen_stack", [])

    if not stack:
        await callback.answer("No previous pages.")
        return

    last = stack.pop()
    await state.update_data(screen_stack=stack)

    # Build markup
    markup = None
    if last["keyboard"]:
        markup = InlineKeyboardMarkup(**last["keyboard"])

    # --- FIX: CHECK IF NEW CONTENT IS SAME AS CURRENT ---
    if callback.message.text == last["text"] and callback.message.reply_markup == markup:
        await callback.answer("Already here.")  # avoid edit and stop
        return
    # ----------------------------------------------------

    try:
        await callback.message.edit_text(last["text"], reply_markup=markup)
    except TelegramBadRequest as e:
        # Secondary safety if Telegram still complains
        if "message is not modified" in e.message:
            await callback.answer()
        else:
            raise
