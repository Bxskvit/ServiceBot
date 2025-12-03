from typing import Optional, List, Tuple
from utils.database_utils import AsyncDatabase


class AsyncOrdersRepository(AsyncDatabase):
    """
    Repository for interacting with the `Orders` table.
    """

    TABLE_NAME = "Orders"

    async def create_order(
        self,
        order_id: int,
        user_id: int,
        item_id: int,
        quantity: int = 1,
        total_price: float = 0,
        profit: Optional[float] = 0,
        payment_method: str = "COD",
        status: str = "Pending",
        notes_and_instructions: Optional[str] = None,
    ) -> None:
        """
        Insert a new order into the Orders table.
        """
        columns = [
            "Order_Id",
            "User_Id",
            "Item_Id",
            "Quantity",
            "Total_Price",
            "Profit",
            "Payment_Method",
            "Status",
            "Notes_and_instructions"
        ]
        values = (
            order_id,
            user_id,
            item_id,
            quantity,
            total_price,
            profit,
            payment_method,
            status,
            notes_and_instructions
        )
        await self.insert(self.TABLE_NAME, columns, values)

    async def get_order_by_id(self, order_id: int) -> Optional[Tuple]:
        """
        Get a single order by Order_Id.
        """
        return await self.get_row(self.TABLE_NAME, "Order_Id = ?", (order_id,))

    async def get_orders_by_user(self, user_id: int) -> List[Tuple]:
        """
        Get all orders for a specific user.
        """
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE User_Id = ?"
        return await self.fetchall(query, (user_id,))

    async def get_all_orders(self) -> List[Tuple]:
        """
        Retrieve all orders.
        """
        return await self.get_table(self.TABLE_NAME)

    async def update_order(
        self,
        order_id: int,
        user_id: Optional[int] = None,
        item_id: Optional[int] = None,
        quantity: Optional[int] = None,
        total_price: Optional[float] = None,
        profit: Optional[float] = None,
        payment_method: Optional[str] = None,
        status: Optional[str] = None,
        notes_and_instructions: Optional[str] = None,
    ) -> None:
        """
        Update order fields. Only non-None fields will be updated.
        """
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
        if total_price is not None:
            updates.append("Total_Price = ?")
            params.append(total_price)
        if profit is not None:
            updates.append("Profit = ?")
            params.append(profit)
        if payment_method is not None:
            updates.append("Payment_Method = ?")
            params.append(payment_method)
        if status is not None:
            updates.append("Status = ?")
            params.append(status)
        if notes_and_instructions is not None:
            updates.append("Notes_and_instructions = ?")
            params.append(notes_and_instructions)

        if updates:
            update_str = ", ".join(updates)
            params.append(order_id)
            await self.update(self.TABLE_NAME, update_str, "Order_Id = ?", tuple(params))

    async def delete_order(self, order_id: int) -> None:
        """
        Delete an order by Order_Id.
        """
        await self.delete(self.TABLE_NAME, "Order_Id = ?", (order_id,))