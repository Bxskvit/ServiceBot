from typing import List, Dict, Optional
from utils.database_utils import (
    AsyncListingsRepository,
    AsyncPCsRepository,
    AsyncLaptopsRepository,
    AsyncPartsRepository
)


async def get_postings(
    db: Optional[AsyncListingsRepository] = None,
    db_path: Optional[str] = None,
    item_type: Optional[str] = None
) -> List[Dict]:
    """
    Fetch listings with titles from the appropriate table depending on item_type.

    Args:
        db (Optional[AsyncListingsRepository]): Existing Listings repo instance.
        db_path (Optional[str]): Path to the database if db is None.
        item_type (Optional[str]): Filter by 'PC', 'Laptop', or 'Part'. Fetch all if None.

    Returns:
        List[Dict]: Listings with main fields + title.
    """

    # Initialize Listings repo if not provided
    if db is None:
        db = AsyncListingsRepository(db_path)

    # Fetch listings, optionally filtered by type
    if item_type:
        listings = await db.get_listings_by_type(item_type)
    else:
        listings = await db.get_all_listings()

    # Initialize repositories for each item type
    pc_repo = AsyncPCsRepository(db_path)
    laptop_repo = AsyncLaptopsRepository(db_path)
    parts_repo = AsyncPartsRepository(db_path)

    result = []

    for listing in listings:
        listing_id, item_type, item_id, added_price, real_price, notes, created_at = listing

        # Fetch title from the corresponding repository
        title = "Unknown"
        if item_type == "PC":
            item = await pc_repo.get_pc(item_id)
            title = item[1] if item else "Unknown PC"
        elif item_type == "Laptop":
            item = await laptop_repo.get_laptop(item_id)
            title = item[1] if item else "Unknown Laptop"
        elif item_type == "Part":
            item = await parts_repo.get_part(item_id)
            title = item[1] if item else "Unknown Part"

        result.append({
            "listing_id": listing_id,
            "item_type": item_type,
            "added_price": added_price,
            "real_price": real_price,
            "title": title,
        })

    return result

