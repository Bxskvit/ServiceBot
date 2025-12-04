from keyboards.kb_generator import create_inline_kb
from utils.database_utils import AsyncListingsRepository, AsyncPCsRepository, AsyncLaptopsRepository, \
    AsyncPartsRepository
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.user_states import BidState

router = Router()

kb = create_inline_kb(1, "go_back")


@router.callback_query(F.data.startswith("bid:"))
async def start_bid(callback: CallbackQuery, state: FSMContext):
    # extract listing_id from callback
    _, listing_id_str = callback.data.split(":")
    listing_id = int(listing_id_str)

    # load listing to get Item_Id and type
    repo = AsyncListingsRepository()
    listing = await repo.get_listing(listing_id)

    if not listing:
        await callback.answer("Listing not found!", show_alert=True)
        return

    # unpack listing row
    _, item_type, item_id, added_price, real_price, notes, created_at = listing

    # fetch the actual item title
    title = "Unknown Item"

    if item_type == "PC":
        pc_repo = AsyncPCsRepository()
        item_details = await pc_repo.get_pc(item_id)
        title = item_details[1] if item_details else "Unknown PC"

    elif item_type == "Laptop":
        laptop_repo = AsyncLaptopsRepository()
        item_details = await laptop_repo.get_laptop(item_id)
        title = item_details[1] if item_details else "Unknown Laptop"

    elif item_type == "Part":
        parts_repo = AsyncPartsRepository()
        item_details = await parts_repo.get_part(item_id)
        title = item_details[1] if item_details else "Unknown Part"

    # store item_id and title in FSM for later
    await state.update_data(item_id=item_id, title=title)

    # set bid state
    await state.set_state(BidState.waiting_for_price)

    # delete previous message
    await callback.message.delete()

    # ask for price
    await callback.message.answer(
        f"💵 Please enter your bid price for <b>{title}</b>:",
        reply_markup=kb,
        parse_mode="html"
    )
