from typing import Optional, Tuple, List, Any
from .database import AsyncDatabase


class AsyncPartsRepository(AsyncDatabase):
    """
    Repository for interacting with the `Parts` table.

    Provides high-level methods for adding, updating, deleting, and fetching parts.
    """

    TABLE = "Parts"

    # ----------------- Getters -----------------

    async def get_part(self, part_id: int) -> Optional[Tuple]:
        """
        Retrieve a single part by Part_Id.

        Args:
            part_id (int): Part ID.

        Returns:
            Optional[Tuple]: Part row or None if not found.
        """
        return await self.get_row(self.TABLE, "Part_Id = ?", (part_id,))

    async def get_all_parts(self) -> List[Tuple[Any]]:
        """
        Retrieve all parts.

        Returns:
            List[Tuple]: All part rows.
        """
        return await self.get_table(self.TABLE)

    async def get_parts_by_type(self, part_type: str) -> List[Tuple[Any]]:
        """
        Retrieve all parts of a given type.

        Args:
            part_type (str): Type of the part (e.g., 'CPU', 'GPU').

        Returns:
            List[Tuple]: List of matching parts.
        """
        query = f"SELECT * FROM {self.TABLE} WHERE Type = ?"
        return await self.fetchall(query, (part_type,))

    # ----------------- Insert / Update / Delete -----------------

    async def add_part(
        self,
        type: str,
        title: str,
        condition: str = "Used",
        listed_price: float = 0,
        sold_price: Optional[float] = None,
        listing_url: Optional[str] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        contact_info: Optional[str] = None,
        contract_id: Optional[float] = None
    ) -> None:
        """
        Insert a new part into the database.

        Args:
            type (str): Part type (must be one of allowed types).
            title (str): Part title.
            condition (str): Part condition ('New', 'Used', etc.).
            listed_price (float): Listed price.
            sold_price (float, optional): Sold price.
            listing_url (str, optional): URL to listing.
            description (str, optional): Description of the part.
            notes (str, optional): Additional notes.
            contact_info (str, optional): Seller contact info.
            contract_id (float, optional): Contract ID if applicable.

        Returns:
            None
        """
        columns = [
            "Type", "Title", "Condition", "Listed_Price", "Sold_Price",
            "Listing_URL", "Description", "Notes", "Contact_Info", "Contract_Id"
        ]
        values = (
            type, title, condition, listed_price, sold_price,
            listing_url, description, notes, contact_info, contract_id
        )
        await self.insert(self.TABLE, columns, values)

    async def update_part(
        self,
        part_id: int,
        updates: str,
        params: Tuple
    ) -> None:
        """
        Update a part by ID.

        Args:
            part_id (int): Part ID.
            updates (str): SET clause, e.g. "Title = ?, Listed_Price = ?"
            params (Tuple): Values for SET clause + part_id at the end.

        Returns:
            None
        """
        await self.update(self.TABLE, updates, "Part_Id = ?", params)

    async def remove_part(self, part_id: int) -> None:
        """
        Delete a part by ID.

        Args:
            part_id (int): Part ID.

        Returns:
            None
        """
        await self.delete(self.TABLE, "Part_Id = ?", (part_id,))