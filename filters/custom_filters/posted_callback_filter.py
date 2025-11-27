from typing import Set
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from utils.database_utils import AsyncComputersRepository


class PostIDFilter(BaseFilter):
    """
    Aiogram filter that dynamically checks if the callback data corresponds
    to an existing computer post ID in the database.

    Usage:
        @router.callback_query(PostIDFilter())
        async def handle_post(callback: CallbackQuery):
            ...
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        Check if the callback's data matches a post ID in the Computers table.

        Args:
            callback (CallbackQuery): The incoming callback query.

        Returns:
            bool: True if the callback.data is a valid post ID, False otherwise.
        """
        repo = AsyncComputersRepository()
        post_ids: Set[int] = set(await repo.get_all_post_ids())
        allowed_posts: Set[str] = {str(pid) for pid in post_ids}

        return callback.data in allowed_posts
