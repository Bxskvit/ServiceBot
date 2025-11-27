from typing import List, Dict
from utils.database_utils import AsyncComputersRepository
from typing import Optional


async def get_postings(db: Optional[AsyncComputersRepository] = None, db_path: Optional[str] = None) -> List[Dict]:
    """
    Fetch all computers with only the main fields needed for posting.

    Args:
        db (AsyncComputersRepository): Repository for the Computers table.
        db_path (Str): Path to database

    Returns:
        List[Dict]: Each dict contains main computer info for posting.
    """

    if db is None:
        db: AsyncComputersRepository = AsyncComputersRepository(db_path)
    else:
        db: AsyncComputersRepository = db

    query = """
        SELECT Post_id, Title, Type, CPU, GPU, RAM, Storage, Price, Screen_Size, OS, Best_Usage, Description, Additional_Info
        FROM Computers
    """
    rows = await db.fetchall(query)

    computers = [
        {
            "post_id": row[0],
            "title": row[1],
            "type": row[2],
            "cpu": row[3],
            "gpu": row[4],
            "ram": row[5],
            "storage": row[6],
            "price": row[7],
            "screen_size": row[8],
            "os": row[9],
            "best_usage": row[10],
            "description": row[11],
            "additional_info": row[12],
        }
        for row in rows
    ]

    return computers
