from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.order_list_utils import format_orders  # updated unified function
from keyboards.kb_generator import create_inline_kb

router: Router = Router()


@router.callback_query(F.data == "my_orders")
async def list_user_orders(callback: CallbackQuery):
    # Telegram user ID
    telegram_user_id = callback.from_user.id

    # Fetch and format orders directly
    formatted_orders = await format_orders(telegram_user_id)

    if not formatted_orders:
        await callback.answer("You have no orders.", show_alert=True)
        return

    # Create inline keyboard with order buttons
    # Here the key can just be the index or Order_Id; we'll use Order_Id
    kwargs = {
        str(i + 1): order_text  # buttons labeled 1, 2, ...; callback data could be i+1 or Order_Id
        for i, order_text in enumerate(formatted_orders)
    }

    kb = create_inline_kb(width=1, **kwargs)
    back_kb = create_inline_kb(1, "go_back")
    kb.inline_keyboard.extend(back_kb.inline_keyboard)

    # Delete previous message and send the orders
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer(
        "Here are your orders:\n",
        reply_markup=kb,
        parse_mode="html"
    )
