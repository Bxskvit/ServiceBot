from utils.database_utils import AsyncBidsRepository
from states.user_states import BidState
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(BidState.waiting_for_price)
async def process_bid_price(message: Message, state: FSMContext):
    # validate price
    try:
        price = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Enter a valid number:")
        return

    data = await state.get_data()
    item_id = data.get("item_id")
    title = data.get("title")

    bids_repo = AsyncBidsRepository()

    await bids_repo.create_bid(
        user_id=message.from_user.id,
        item_id=item_id,
        quantity=1,
        offered_price=price,
        notes_and_instructions=None,
        status="Pending"
    )

    await state.clear()

    await message.answer(
        f"Your bid of <b>{price}</b> has been submitted!\n"
        f"Unit: <b>{title}</b>",
        parse_mode="html"
    )
