from typing import Optional, List, Tuple
from utils.database_utils import AsyncDatabase


class AsyncBidsRepository(AsyncDatabase):
    """
    Repository for interacting with the `Bids` table.
    """

    TABLE_NAME = "Bids"

    async def create_bid(
        self,
        user_id: int,
        item_id: int,
        quantity: int,
        offered_price: float,
        notes_and_instructions: Optional[str] = None,
        status: str = "Pending"
    ) -> None:
        """
        Insert a new bid into the Bids table.
        """
        columns = [
            "User_Id",
            "Item_Id",
            "Quantity",
            "Offered_Price",
            "Notes_and_instructions",
            "Status"
        ]
        values = (
            user_id,
            item_id,
            quantity,
            offered_price,
            notes_and_instructions,
            status
        )
        await self.insert(self.TABLE_NAME, columns, values)

    async def get_bid_by_id(self, bid_id: int) -> Optional[Tuple]:
        return await self.get_row(self.TABLE_NAME, "Bid_Id = ?", (bid_id,))

    async def get_bids_by_user(self, user_id: int) -> List[Tuple]:
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE User_Id = ?"
        return await self.fetchall(query, (user_id,))

    async def get_all_bids(self) -> List[Tuple]:
        return await self.get_table(self.TABLE_NAME)

    async def update_bid(
        self,
        bid_id: int,
        user_id: Optional[int] = None,
        item_id: Optional[int] = None,
        quantity: Optional[int] = None,
        offered_price: Optional[float] = None,
        status: Optional[str] = None,
        notes_and_instructions: Optional[str] = None,
    ) -> None:

        updates = []
        params = []

        if user_id is not None:
            updates.append("User_Id = ?")
            params.append(user_id)
        if item_id is not None:
            updates.append("Item_Id = ?")
            params.append(item_id)
        if quantity is not None:
            updates.append("Quantity = ?")
            params.append(quantity)
        if offered_price is not None:
            updates.append("Offered_Price = ?")
            params.append(offered_price)
        if status is not None:
            updates.append("Status = ?")
            params.append(status)
        if notes_and_instructions is not None:
            updates.append("Notes_and_instructions = ?")
            params.append(notes_and_instructions)

        if updates:
            update_str = ", ".join(updates)
            params.append(bid_id)
            await self.update(self.TABLE_NAME, update_str, "Bid_Id = ?", tuple(params))

    async def delete_bid(self, bid_id: int) -> None:
        await self.delete(self.TABLE_NAME, "Bid_Id = ?", (bid_id,))