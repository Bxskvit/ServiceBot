from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from utils.database_utils import AsyncListingsRepository


class PostIDFilter(BaseFilter):
    """
    Aiogram filter that dynamically checks if the callback data corresponds
    to an existing listing ID in the Listings table.

    Usage:
        @router.callback_query(PostIDFilter())
        async def handle_post(callback: CallbackQuery):
            ...
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        Check if the callback's data matches a Listing ID in the database.

        Args:
            callback (CallbackQuery): The incoming callback query.

        Returns:
            bool: True if the callback data is a valid Listing ID, False otherwise.
        """
        repo = AsyncListingsRepository()
        listings = await repo.get_all_listings()
        listed_units = {str(row[0]) for row in listings}  # row[0] is Listing_Id

        return callback.data in listed_units
