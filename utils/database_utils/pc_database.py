from .database import AsyncDatabase
from typing import Optional, Tuple, List, Any


class AsyncPCsRepository(AsyncDatabase):
    TABLE = "PCs"

    async def get_pc(self, pc_id: int) -> Optional[Tuple]:
        return await self.get_row(self.TABLE, "PC_Id = ?", (pc_id,))

    async def get_all_pcs(self) -> List[Tuple[Any]]:
        return await self.get_table(self.TABLE)

    async def add_pc(
        self,
        title: str,
        cpu_id: int,
        gpu_id: int,
        ram_id: int,
        ssd_id: Optional[int] = None,
        hdd_id: Optional[int] = None,
        psu_id: Optional[int] = None,
        motherboard_id: Optional[int] = None,
        case_id: Optional[int] = None,
        cooler_id: Optional[int] = None,
        fan_id: Optional[int] = None,
        photo_url: Optional[str] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        condition: str = "Used"
    ) -> None:
        columns = [
            "Title", "CPU_Id", "GPU_Id", "RAM_Id", "SSD_Id", "HDD_Id",
            "PSU_Id", "Motherboard_Id", "Case_Id", "Cooler_Id", "Fan_Id",
            "Photo_URL", "Description", "Notes", "Condition"
        ]
        values = (
            title, cpu_id, gpu_id, ram_id, ssd_id, hdd_id,
            psu_id, motherboard_id, case_id, cooler_id, fan_id,
            photo_url, description, notes, condition
        )
        await self.insert(self.TABLE, columns, values)

    async def update_pc(
        self,
        pc_id: int,
        title: Optional[str] = None,
        cpu_id: Optional[int] = None,
        gpu_id: Optional[int] = None,
        ram_id: Optional[int] = None,
        ssd_id: Optional[int] = None,
        hdd_id: Optional[int] = None,
        psu_id: Optional[int] = None,
        motherboard_id: Optional[int] = None,
        case_id: Optional[int] = None,
        cooler_id: Optional[int] = None,
        fan_id: Optional[int] = None,
        photo_url: Optional[str] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        condition: Optional[str] = None
    ) -> None:
        updates = []
        params = []

        mapping = {
            "Title": title, "CPU_Id": cpu_id, "GPU_Id": gpu_id, "RAM_Id": ram_id,
            "SSD_Id": ssd_id, "HDD_Id": hdd_id, "PSU_Id": psu_id,
            "Motherboard_Id": motherboard_id, "Case_Id": case_id, "Cooler_Id": cooler_id,
            "Fan_Id": fan_id, "Photo_URL": photo_url, "Description": description,
            "Notes": notes, "Condition": condition
        }

        for col, val in mapping.items():
            if val is not None:
                updates.append(f"{col} = ?")
                params.append(val)

        if not updates:
            return  # nothing to update

        params.append(pc_id)
        await self.update(self.TABLE, ", ".join(updates), "PC_Id = ?", tuple(params))

    async def delete_pc(self, pc_id: int) -> None:
        await self.delete(self.TABLE, "PC_Id = ?", (pc_id,))