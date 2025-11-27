from .database import AsyncDatabase
from typing import Optional, Tuple, List, Any


class AsyncAdminsRepository(AsyncDatabase):
    """
    Repository for interacting with the `Admins` table.

    This class provides high-level, typed methods for reading and modifying
    administrator records without writing raw SQL in the rest of the project.

    Inherits:
        AsyncDatabase – asynchronous base class providing generic
        CRUD operations and query helpers.
    """

    TABLE = "Admins"

    async def get_admin(self, user_id: int) -> Optional[Tuple]:
        """
        Retrieve a single admin by user ID.

        Args:
            user_id (int): Telegram user ID.

        Returns:
            Optional[Tuple]: Row of the admin record,
            or None if no such admin exists.
        """
        return await self.get_row(self.TABLE, "User_Id = ?", (user_id,))

    async def get_all_admins(self) -> List[Tuple[Any]]:
        """
        Retrieve all admin records from the database.

        Returns:
            list[Tuple]: A list of all rows in the `Admins` table.
        """
        return await self.get_table(self.TABLE)

    async def add_admin(self, user_id: int, access_level: int, name: str = None) -> None:
        """
        Add a new admin to the database.

        Args:
            user_id (int): Telegram user ID of the admin.
            access_level (int): Access level (1, 2, or 3).
            name (str, optional): Display name of the admin.

        Returns:
            None
        """
        await self.insert(
            self.TABLE,
            ["User_Id", "Name", "Access_Level"],
            (user_id, name, access_level)
        )

    async def remove_admin(self, user_id: int) -> None:
        """
        Remove an admin by user ID.

        Args:
            user_id (int): Telegram user ID to remove.

        Returns:
            None
        """
        await self.delete(
            self.TABLE,
            "User_Id = ?",
            (user_id,)
        )

    async def update_access(self, user_id: int, new_level: int) -> None:
        """
        Update an admin's access level.

        Args:
            user_id (int): Telegram user ID.
            new_level (int): New access level (1–3).

        Returns:
            None
        """
        await self.update(
            self.TABLE,
            "Access_Level = ?",
            "User_Id = ?",
            (new_level, user_id)
        )
