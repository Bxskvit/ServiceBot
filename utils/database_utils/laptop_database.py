from typing import Optional, Tuple, List, Any
from utils.database_utils import AsyncDatabase


class AsyncLaptopsRepository(AsyncDatabase):
    """
    Repository for interacting with the `Laptops` table.

    Provides typed, high-level methods for reading and modifying
    laptop records.
    """

    TABLE = "Laptops"

    # ----------------- Getters -----------------

    async def get_laptop(self, laptop_id: int) -> Optional[Tuple]:
        """
        Retrieve a single laptop by ID.

        Args:
            laptop_id (int): Laptop ID.

        Returns:
            Optional[Tuple]: Laptop row or None if not found.
        """
        return await self.get_row(self.TABLE, "Laptop_Id = ?", (laptop_id,))

    async def get_all_laptops(self) -> List[Tuple[Any]]:
        """
        Retrieve all laptops.

        Returns:
            List[Tuple]: List of all laptop rows.
        """
        return await self.get_table(self.TABLE)

    # ----------------- Insert / Update / Delete -----------------

    async def add_laptop(
        self,
        title: str,
        cpu_id: Optional[int] = None,
        gpu_id: Optional[int] = None,
        ram_id: Optional[int] = None,
        ssd_id: Optional[int] = None,
        hdd_id: Optional[int] = None,
        motherboard_id: Optional[int] = None,
        battery_id: Optional[int] = None,
        keyboard_id: Optional[int] = None,
        touchpad_id: Optional[int] = None,
        display_id: Optional[int] = None,
        charger_id: Optional[int] = None,
        webcam_id: Optional[int] = None,
        case_panel_id: Optional[int] = None,
        photo_url: Optional[str] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        condition: str = "Used"
    ) -> None:
        """
    Insert a new laptop into the database.

    Args:
        title (str): Laptop title.
        cpu_id (Optional[int]): ID of CPU part.
        gpu_id (Optional[int]): ID of GPU part.
        ram_id (Optional[int]): ID of RAM part.
        ssd_id (Optional[int]): ID of SSD part.
        hdd_id (Optional[int]): ID of HDD part.
        motherboard_id (Optional[int]): ID of Motherboard part.
        battery_id (Optional[int]): ID of Battery part.
        keyboard_id (Optional[int]): ID of Keyboard part.
        touchpad_id (Optional[int]): ID of Touchpad part.
        display_id (Optional[int]): ID of Display part.
        charger_id (Optional[int]): ID of Charger part.
        webcam_id (Optional[int]): ID of Webcam part.
        case_panel_id (Optional[int]): ID of Case Panel part.
        photo_url (Optional[str]): URL to laptop photo.
        description (Optional[str]): Description of the laptop.
        notes (Optional[str]): Additional notes.
        condition (str): Condition of the laptop. One of 'New', 'Used', 'Open-Box', 'For-Parts'.

    Returns:
        None
    """

        columns = [
            "Title", "CPU_Id", "GPU_Id", "RAM_Id", "SSD_Id", "HDD_Id",
            "Motherboard_Id", "Battery_Id", "Keyboard_Id", "Touchpad_Id",
            "Display_Id", "Charger_Id", "Webcam_Id", "Case_Panel_Id",
            "Photo_URL", "Description", "Notes", "Condition"
        ]
        values = (
            title, cpu_id, gpu_id, ram_id, ssd_id, hdd_id,
            motherboard_id, battery_id, keyboard_id, touchpad_id,
            display_id, charger_id, webcam_id, case_panel_id,
            photo_url, description, notes, condition
        )

        await self.insert(self.TABLE, columns, values)

    async def update_laptop(
        self,
        laptop_id: int,
        updates: str,
        params: Tuple
    ) -> None:
        """
        Update fields for a laptop by ID.

        Args:
            laptop_id (int): Laptop ID.
            updates (str): SET clause, e.g. "Title = ?, CPU_Id = ?"
            params (Tuple): Values for SET clause + ID at the end.

        Returns:
            None
        """
        await self.update(self.TABLE, updates, "Laptop_Id = ?", params)

    async def remove_laptop(self, laptop_id: int) -> None:
        """
        Delete a laptop by ID.

        Args:
            laptop_id (int): Laptop ID.

        Returns:
            None
        """
        await self.delete(self.TABLE, "Laptop_Id = ?", (laptop_id,))
