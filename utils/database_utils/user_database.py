from typing import Optional, List, Tuple
from utils.database_utils import AsyncDatabase  # assuming your base class is in base_database.py


class AsyncUsersRepository(AsyncDatabase):
    """
    Repository for interacting with the `Users` table.
    """

    TABLE_NAME = "Users"

    async def create_user(
        self,
        user_id: int,
        username: str,
        name: str,
        company_id: Optional[int] = None,
        level: int = 1,
        type_: str = "Individual",
        address: Optional[str] = None,
        contact_info: Optional[str] = None,
    ) -> None:
        """
        Insert a new user into the Users table.
        """
        columns = ["User_Id", "Username", "Name", "Company_Id", "Level", "Type", "Address", "Contact_info"]
        values = (user_id, username, name, company_id, level, type_, address, contact_info)
        await self.insert(self.TABLE_NAME, columns, values)

    async def get_user_by_id(self, user_id: int) -> Optional[Tuple]:
        """
        Get a single user by their User_Id.
        """
        return await self.get_row(self.TABLE_NAME, "User_Id = ?", (user_id,))

    async def get_all_users(self) -> List[Tuple]:
        """
        Retrieve all users.
        """
        return await self.get_table(self.TABLE_NAME)

    async def update_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        name: Optional[str] = None,
        company_id: Optional[int] = None,
        level: Optional[int] = None,
        type_: Optional[str] = None,
        address: Optional[str] = None,
        contact_info: Optional[str] = None,
    ) -> None:
        """
        Update user fields. Only non-None fields will be updated.
        """
        updates = []
        params = []

        if username is not None:
            updates.append("Username = ?")
            params.append(username)
        if name is not None:
            updates.append("Name = ?")
            params.append(name)
        if company_id is not None:
            updates.append("Company_Id = ?")
            params.append(company_id)
        if level is not None:
            updates.append("Level = ?")
            params.append(level)
        if type_ is not None:
            updates.append("Type = ?")
            params.append(type_)
        if address is not None:
            updates.append("Address = ?")
            params.append(address)
        if contact_info is not None:
            updates.append("Contact_info = ?")
            params.append(contact_info)

        if updates:
            update_str = ", ".join(updates)
            params.append(user_id)
            await self.update(self.TABLE_NAME, update_str, "User_Id = ?", tuple(params))

    async def delete_user(self, user_id: int) -> None:
        """
        Delete a user by their User_Id.
        """
        await self.delete(self.TABLE_NAME, "User_Id = ?", (user_id,))