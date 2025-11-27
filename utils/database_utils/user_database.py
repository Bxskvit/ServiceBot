from typing import Optional, Tuple, List
from utils.database_utils import AsyncDatabase  # base class


class AsyncUsersRepository(AsyncDatabase):
    """
    Repository for interacting with the `Users` table.

    Table structure:
        Users(User_Id PRIMARY KEY, Name TEXT, Company TEXT)
    """

    TABLE = "Users"

    async def get_user(self, user_id: int) -> Optional[Tuple[int, Optional[str], Optional[str]]]:
        """
        Fetch a single user by User_Id.

        Args:
            user_id (int): Telegram user ID.

        Returns:
            Optional[Tuple[int, Optional[str], Optional[str]]]:
                User row (User_Id, Name, Company) or None if user does not exist.
        """
        return await self.get_row(self.TABLE, "User_Id = ?", (user_id,))

    async def get_all_users(self) -> List[Tuple[int, Optional[str], Optional[str]]]:
        """
        Fetch all users.

        Returns:
            List[Tuple[int, Optional[str], Optional[str]]]:
                List of all rows in Users table.
        """
        return await self.get_table(self.TABLE)

    async def add_user(self, user_id: int, name: Optional[str] = None, company: Optional[str] = None) -> None:
        """
        Add a new user.

        Args:
            user_id (int): Telegram user ID.
            name (Optional[str]): User's name.
            company (Optional[str]): User's company.

        Returns:
            None
        """
        await self.insert(
            self.TABLE,
            ["User_Id", "Name", "Company"],
            (user_id, name, company)
        )

    async def remove_user(self, user_id: int) -> None:
        """
        Remove a user by User_Id.

        Args:
            user_id (int): Telegram user ID.

        Returns:
            None
        """
        await self.delete(self.TABLE, "User_Id = ?", (user_id,))
