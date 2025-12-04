from aiogram import Router
from aiogram.types import CallbackQuery
from filters.custom_filters import PostIDFilter
from utils.database_utils import AsyncListingsRepository, AsyncPCsRepository, AsyncLaptopsRepository, AsyncPartsRepository
from utils.computer_list_utils import format_computer_description_message
from keyboards.kb_generator import create_inline_kb

router = Router()


@router.callback_query(PostIDFilter())  # dynamically checks if callback is a valid listing ID
async def handle_post_id(callback: CallbackQuery):
    listing_id = int(callback.data)

    kwargs = {
        f"bid:{listing_id}": "Bid"
    }
    kb = create_inline_kb(width=1, **kwargs)  # main bid button

    # Create back button keyboard
    back_kb = create_inline_kb(1, "go_back")

    # Merge back button row into main kb
    kb.inline_keyboard.extend(back_kb.inline_keyboard)

    # Initialize repositories
    listings_repo = AsyncListingsRepository()
    listing = await listings_repo.get_listing(listing_id)

    if not listing:
        await callback.answer("Listing not found!", show_alert=True)
        return

    _, item_type, item_id, added_price, real_price, notes, created_at = listing

    # Fetch actual item info from the correct table
    title = "Unknown"
    item_details = None

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

    # Format description
    description = format_computer_description_message(
        item=item_details or listing,  # fallback to listing info if details not found
        item_type=item_type,
        added_price=added_price,
        real_price=real_price,
        notes=notes
    )

    await callback.message.delete()
    await callback.answer(f"You clicked on listing ID: {listing_id}")
    await callback.message.answer(
        f"{description}",
        reply_markup=kb,
        parse_mode='html'
    )