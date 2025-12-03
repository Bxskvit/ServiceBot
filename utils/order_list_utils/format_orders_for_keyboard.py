from typing import List, Dict, Optional
from utils.database_utils import AsyncOrdersRepository, AsyncUsersRepository, AsyncAdminsRepository

orders_repo = AsyncOrdersRepository()
users_repo = AsyncUsersRepository()
admins_repo = AsyncAdminsRepository()


async def format_orders(user_id: Optional[int] = None) -> List[str]:
    """
    Retrieve and format orders.

    - If `user_id` is given and the user is not an admin, returns only that user's orders.
    - If the user is an admin or `user_id` is None, returns all orders with user info.

    Returns:
        List[str]: Human-readable formatted order strings.
    """
    is_admin = False
    if user_id:
        admin_row = await admins_repo.get_admin_by_user_id(user_id)
        if admin_row:
            is_admin = True

    # Get orders
    if user_id and not is_admin:
        orders_rows = await orders_repo.get_orders_by_user(user_id)
    else:
        orders_rows = await orders_repo.get_all_orders()

    if not orders_rows:
        return []

    # Keys for Orders table
    order_keys = ["Order_Id", "User_Id", "Item_Id", "Quantity", "Total_Price",
                  "Profit", "Payment_Method", "Status", "Notes_and_instructions", "Created_At"]

    formatted_orders = []
    for i, row in enumerate(orders_rows, start=1):
        order = dict(zip(order_keys, row))
        user_info = ""

        # Include user info if returning all orders
        if not user_id or is_admin:
            user_row = await users_repo.get_user_by_id(order["User_Id"])
            if user_row:
                u_keys = ["User_Id", "Username", "Name", "Company_Id", "Level", "Type", "Address", "Contact_info",
                          "Created_At"]
                user_dict = dict(zip(u_keys, user_row))
                user_info = f"{user_dict.get('Name') or user_dict.get('Username')} (ID: {order['User_Id']})\n"

        lines = [
            f"{i}) {user_info}Order ID: {order['Order_Id']}",
            f"Item ID: {order['Item_Id']}",
            f"Quantity: {order['Quantity']}",
            f"Total Price: ${order['Total_Price']}",
            f"Profit: ${order['Profit']}",
            f"Payment Method: {order['Payment_Method']}",
            f"Status: {order['Status']}",
        ]
        if order.get("Notes_and_instructions"):
            lines.append(f"Notes: {order['Notes_and_instructions']}")
        formatted_orders.append("\n".join(lines))

    return formatted_orders
