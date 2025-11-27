from typing import List, Dict


async def format_computers(computers: List[Dict]) -> List[str]:
    """
    Convert a list of computer dicts into a list of human-readable strings,
    one per computer, with a number prefix (1), 2), ...).

    Args:
        computers (List[Dict]): List of dicts, each with computer info.

    Returns:
        List[str]: Each string contains formatted info for one computer.
    """
    def format_computer(index: int, pc: Dict) -> str:
        lines = [
            f"{index}) {pc.get('title', 'Unknown')}",
            f"Type: {pc.get('type', '-')}",
            f"CPU: {pc.get('cpu', '-')}",
            f"GPU: {pc.get('gpu', '-')}",
            f"RAM: {pc.get('ram', '-')}",
            f"Storage: {pc.get('storage', '-')}",
            f"Price: ${pc.get('price', '-')}"
        ]

        if pc.get('screen_size'):
            lines.append(f"Screen Size: {pc['screen_size']} inches")
        if pc.get('os'):
            lines.append(f"OS: {pc['os']}")
        if pc.get('best_usage'):
            lines.append(f"Best Usage: {pc['best_usage']}")
        if pc.get('description'):
            lines.append(f"Description: {pc['description']}")
        if pc.get('additional_info'):
            lines.append(f"Additional Info: {pc['additional_info']}")

        return " \n".join(lines)

    # Return a list of strings, one per computer, numbered
    return [format_computer(i + 1, pc) for i, pc in enumerate(computers)]
