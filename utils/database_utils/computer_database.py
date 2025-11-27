from typing import Optional, Tuple, List
from utils.database_utils import AsyncDatabase


class AsyncComputersRepository(AsyncDatabase):
    """
    Repository for interacting with the `Computers` table.

    Table structure:
        Computers(
            Post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT,
            Type TEXT NOT NULL,
            CPU TEXT NOT NULL,
            CPU_Fan TEXT,
            Motherboard TEXT,
            GPU TEXT,
            RAM TEXT,
            Storage TEXT,
            PSU TEXT,
            PC_Case TEXT,
            Screen_Size REAL,
            Display_Type TEXT,
            OS TEXT,
            Connectivity TEXT,
            Ports TEXT,
            Weight REAL,
            Battery TEXT,
            Price REAL NOT NULL,
            Best_Usage TEXT,
            Additional_Info TEXT,
            Post_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    TABLE = "Computers"

    async def get_computer(self, post_id: int) -> Optional[Tuple]:
        """
        Fetch a single computer by Post_id.

        Args:
            post_id (int): ID of the computer post.

        Returns:
            Optional[Tuple]: Row of the computer or None if not found.
        """
        return await self.get_row(self.TABLE, "Post_id = ?", (post_id,))

    async def get_all_computers(self) -> List[Tuple]:
        """
        Fetch all computers in the table.

        Returns:
            List[Tuple]: List of all rows in Computers table.
        """
        return await self.get_table(self.TABLE)

    async def add_computer(
            self,
            title: str,
            type_: str,
            cpu: str,
            price: float,
            description: Optional[str] = None,
            cpu_fan: Optional[str] = None,
            motherboard: Optional[str] = None,
            gpu: Optional[str] = None,
            ram: Optional[str] = None,
            storage: Optional[str] = None,
            psu: Optional[str] = None,
            pc_case: Optional[str] = None,
            screen_size: Optional[float] = None,
            display_type: Optional[str] = None,
            os: Optional[str] = None,
            connectivity: Optional[str] = None,
            ports: Optional[str] = None,
            weight: Optional[float] = None,
            battery: Optional[str] = None,
            best_usage: Optional[str] = None,
            additional_info: Optional[str] = None
    ) -> None:
        """
        Add a new computer post to the database.

        Args:
            title (str): Computer title.
            type_ (str): Type of computer, either "Laptop" or "PC".
            cpu (str): CPU model.
            price (float): Price of the computer.
            description (Optional[str]): Detailed description of the computer.
            cpu_fan (Optional[str]): CPU cooler/fan model.
            motherboard (Optional[str]): Motherboard model.
            gpu (Optional[str]): Graphics card model.
            ram (Optional[str]): RAM configuration.
            storage (Optional[str]): Storage configuration.
            psu (Optional[str]): Power supply unit.
            pc_case (Optional[str]): Computer case.
            screen_size (Optional[float]): Screen size in inches (for laptops/monitors).
            display_type (Optional[str]): Display type (e.g., IPS, OLED, TN).
            os (Optional[str]): Operating system.
            connectivity (Optional[str]): Network connectivity info (WiFi, Ethernet, Bluetooth).
            ports (Optional[str]): Ports available (USB, HDMI, etc.).
            weight (Optional[float]): Weight in kg.
            battery (Optional[str]): Battery info (for laptops).
            best_usage (Optional[str]): Recommended use case (e.g., gaming, office).
            additional_info (Optional[str]): Any additional information.

        Returns:
            None
        """
        await self.insert(
            self.TABLE,
            [
                "Title", "Description", "Type", "CPU", "CPU_Fan", "Motherboard", "GPU",
                "RAM", "Storage", "PSU", "PC_Case", "Screen_Size", "Display_Type", "OS",
                "Connectivity", "Ports", "Weight", "Battery", "Price", "Best_Usage",
                "Additional_Info"
            ],
            (
                title, description, type_, cpu, cpu_fan, motherboard, gpu,
                ram, storage, psu, pc_case, screen_size, display_type, os,
                connectivity, ports, weight, battery, price, best_usage,
                additional_info
            )
        )

    async def update_computer(
        self,
        post_id: int,
        updates: str,
        params: Tuple
    ) -> None:
        """
        Update fields of a computer post.

        Args:
            post_id (int): ID of the post to update.
            updates (str): SQL SET clause, e.g., "Price = ?, RAM = ?".
            params (Tuple): Values for the SET clause plus post_id for WHERE.
        """
        await self.update(self.TABLE, updates, "Post_id = ?", params + (post_id,))

    async def remove_computer(self, post_id: int) -> None:
        """
        Delete a computer post by ID.

        Args:
            post_id (int): ID of the post to delete.
        """
        await self.delete(self.TABLE, "Post_id = ?", (post_id,))
