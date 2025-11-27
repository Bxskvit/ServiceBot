from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Optional
from utils.database_utils import AsyncAdminsRepository


class AccessLevelFilter(BaseFilter):
    """
    Aiogram filter to allow only admins with a minimum access level.

    This filter checks the user's access level from the `Admins` table
    and allows the handler to proceed only if the access level
    meets or exceeds the required minimum.

    Args:
        min_level (int): Minimum access level required (1 = highest, 3 = lowest).
        db (Optional[AsyncAdminsRepository]): Optional database repository instance.
        db_path (Optional[str]): Optional path to database (used if `db` not provided).

    Example:
        @dp.message_handler(AccessLevelFilter(min_level=2))
        async def handler(message: Message):
            await message.reply("You have sufficient access level.")
    """

    def __init__(
        self,
        min_level: int = 1,
        db: Optional[AsyncAdminsRepository] = None,
        db_path: Optional[str] = None
    ):
        if db is None:
            self.db: AsyncAdminsRepository = AsyncAdminsRepository(db_path)
        else:
            self.db: AsyncAdminsRepository = db
        self.min_level = min_level

    async def __call__(self, message: Message) -> bool:
        """
        Check if the user meets the required access level.

        Args:
            message (Message): Incoming Telegram message.

        Returns:
            bool: True if user is admin and access level is sufficient, False otherwise.
        """
        user_id = message.from_user.id

        # Fetch admin record
        admin = await self.db.get_admin(user_id)
        if admin is None:
            return False  # User is not an admin

        access_level = admin[1]  # Index 1 = Access_Level column
        return access_level <= self.min_level
