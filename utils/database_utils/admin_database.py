from typing import Optional, List, Tuple
from utils.database_utils import AsyncDatabase


class AsyncAdminsRepository(AsyncDatabase):
    """
    Repository for interacting with the `Admins` table.
    """

    TABLE_NAME = "Admins"

    async def create_admin(
        self,
        user_id: int,
        admin_id: Optional[int],
        admin_name: str,
        access_level: int
    ) -> None:
        """
        Insert a new admin into the Admins table.
        """
        columns = ["User_Id", "Admin_Id", "Admin_name", "Access_Level"]
        values = (user_id, admin_id, admin_name, access_level)
        await self.insert(self.TABLE_NAME, columns, values)

    async def get_admin_by_user_id(self, user_id: int) -> Optional[Tuple]:
        """
        Get a single admin by User_Id.
        """
        return await self.get_row(self.TABLE_NAME, "User_Id = ?", (user_id,))

    async def get_admin_by_admin_id(self, admin_id: int) -> Optional[Tuple]:
        """
        Get a single admin by Admin_Id.
        """
        return await self.get_row(self.TABLE_NAME, "Admin_Id = ?", (admin_id,))

    async def get_all_admins(self) -> List[Tuple]:
        """
        Retrieve all admins.
        """
        return await self.get_table(self.TABLE_NAME)

    async def update_admin(
        self,
        user_id: int,
        admin_id: Optional[int] = None,
        admin_name: Optional[str] = None,
        access_level: Optional[int] = None
    ) -> None:
        """
        Update admin fields. Only non-None fields will be updated.
        """
        updates = []
        params = []

        if admin_id is not None:
            updates.append("Admin_Id = ?")
            params.append(admin_id)
        if admin_name is not None:
            updates.append("Admin_name = ?")
            params.append(admin_name)
        if access_level is not None:
            updates.append("Access_Level = ?")
            params.append(access_level)

        if updates:
            update_str = ", ".join(updates)
            params.append(user_id)
            await self.update(self.TABLE_NAME, update_str, "User_Id = ?", tuple(params))

    async def delete_admin(self, user_id: int) -> None:
        """
        Delete an admin by User_Id.
        """
        await self.delete(self.TABLE_NAME, "User_Id = ?", (user_id,))
