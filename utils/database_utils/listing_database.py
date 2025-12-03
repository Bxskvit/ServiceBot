from utils.database_utils import AsyncDatabase
from typing import Optional, Tuple, List, Any


class AsyncListingsRepository(AsyncDatabase):
    """
    Repository for interacting with the `Listings` table.

    Provides typed async methods for reading, inserting, updating,
    and deleting listing records.
    """

    TABLE = "Listings"

    async def get_listing(self, listing_id: int) -> Optional[Tuple]:
        """
        Retrieve a single listing by Listing_Id.
        """
        return await self.get_row(self.TABLE, "Listing_Id = ?", (listing_id,))

    async def get_all_listings(self) -> List[Tuple[Any]]:
        """
        Retrieve all listings from the database.
        """
        return await self.get_table(self.TABLE)

    async def get_listings_by_type(self, item_type: str) -> List[Tuple[Any]]:
        """
        Retrieve all listings of a specific type (PC, Laptop, Part).
        """
        return await self.fetchall(f"SELECT * FROM {self.TABLE} WHERE Item_Type = ?", (item_type,))

    async def add_listing(
        self,
        item_type: str,
        item_id: int,
        added_price: float = 0,
        real_price: float = 0,
        notes: Optional[str] = None
    ) -> None:
        """
        Add a new listing to the database.
        """
        await self.insert(
            self.TABLE,
            ["Item_Type", "Item_Id", "Added_Price", "Real_Price", "Notes"],
            (item_type, item_id, added_price, real_price, notes)
        )

    async def remove_listing(self, listing_id: int) -> None:
        """
        Remove a listing by its Listing_Id.
        """
        await self.delete(self.TABLE, "Listing_Id = ?", (listing_id,))

    async def update_listing(
        self,
        listing_id: int,
        added_price: Optional[float] = None,
        real_price: Optional[float] = None,
        notes: Optional[str] = None
    ) -> None:
        """
        Update fields of a listing.
        Only updates the fields provided (non-None).
        """
        updates = []
        params = []

        if added_price is not None:
            updates.append("Added_Price = ?")
            params.append(added_price)
        if real_price is not None:
            updates.append("Real_Price = ?")
            params.append(real_price)
        if notes is not None:
            updates.append("Notes = ?")
            params.append(notes)

        if not updates:
            return  # nothing to update

        updates_str = ", ".join(updates)
        params.append(listing_id)

        await self.update(self.TABLE, updates_str, "Listing_Id = ?", tuple(params))
