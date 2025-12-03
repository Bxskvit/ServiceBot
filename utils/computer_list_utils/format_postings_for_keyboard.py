from typing import List, Dict


async def format_computers(items: List[Dict]) -> List[str]:
    """
    Convert a list of listing dicts into human-readable strings,
    numbered 1), 2), etc., for all item types (PC, Laptop, Part).

    Args:
        items (List[Dict]): List of dicts, each with listing info.

    Returns:
        List[str]: Formatted strings for each listing.
    """

    def format_item(index: int, item: Dict) -> str:
        lines = [
            f"{index}) {item.get('title', 'Unknown')}",
            f"Type: {item.get('item_type', '-')}",
            f"Price: ${item.get('added_price', '-')}"
        ]

        if item.get('notes'):
            lines.append(f"Notes: {item['notes']}")

        return " \n".join(lines)

    return [format_item(i + 1, item) for i, item in enumerate(items)]
