from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Optional
from utils.database_utils import AsyncUsersRepository, AsyncAdminsRepository


class AllowedUserFilter(BaseFilter):
    """
    Aiogram filter to allow users present in the `Users` table
    or admins present in the `Admins` table.
    """

    def __init__(
        self,
        users_repo: Optional[AsyncUsersRepository] = None,
        admins_repo: Optional[AsyncAdminsRepository] = None,
        db_path: Optional[str] = None
    ):
        """
        Initialize filter.

        Args:
            users_repo (Optional[AsyncUsersRepository]): Pre-initialized Users repository.
            admins_repo (Optional[AsyncAdminsRepository]): Pre-initialized Admins repository.
            db_path (Optional[str]): Database path if repositories are not provided.
        """
        self.users_repo: AsyncUsersRepository = users_repo or AsyncUsersRepository(db_path)
        self.admins_repo: AsyncAdminsRepository = admins_repo or AsyncAdminsRepository(db_path)

    async def __call__(self, message: Message) -> bool:
        """
        Check if the user exists in Users or is an Admin.

        Args:
            message (Message): Incoming Telegram message.

        Returns:
            bool: True if user exists in Users or Admins, False otherwise.
        """
        user_id = message.from_user.id

        # Check Users table
        user = await self.users_repo.get_user(user_id)
        if user is not None:
            return True

        # Check Admins table
        admin = await self.admins_repo.get_admin(user_id)
        return admin is not None
