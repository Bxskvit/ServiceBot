
def format_computer_description_message(
    item: tuple,
    item_type: str,
    added_price: float = None,
    real_price: float = None,
    notes: str = None
) -> str:
    """
    Format a PC, Laptop, or Part row into a Telegram-friendly message.

    Args:
        item (tuple): Row from the corresponding table.
        item_type (str): 'PC', 'Laptop', or 'Part'.
        added_price (float, optional): Listing added price.
        real_price (float, optional): Listing real price.
        notes (str, optional): Notes from the listing.

    Returns:
        str: Formatted message.
    """

    message_lines = []

    # Basic title
    title = item[1] if item else "Unknown"
    message_lines.append(f"<b>{title}</b>")

    # Optional notes / description
    if notes:
        message_lines.append(f"{notes}\n")

    # Type
    message_lines.append(f"<b>Type:</b> {item_type}")

    # Type-specific fields
    if item_type == "PC":
        (
            PC_Id, Title, CPU_Id, GPU_Id, RAM_Id, SSD_Id, HDD_Id, PSU_Id,
            Motherboard_Id, Case_Id, Cooler_Id, Fan_Id, Photo_URL,
            Description, Notes_field, Condition, Created_At
        ) = item

        message_lines.append(f"<b>Condition:</b> {Condition}")
        message_lines.append(f"<b>CPU ID:</b> {CPU_Id}")
        message_lines.append(f"<b>GPU ID:</b> {GPU_Id}")
        message_lines.append(f"<b>RAM ID:</b> {RAM_Id}")
        message_lines.append(f"<b>Storage SSD ID:</b> {SSD_Id}")
        message_lines.append(f"<b>Storage HDD ID:</b> {HDD_Id}")
        message_lines.append(f"<b>PSU ID:</b> {PSU_Id}")
        message_lines.append(f"<b>Motherboard ID:</b> {Motherboard_Id}")
        message_lines.append(f"<b>Case ID:</b> {Case_Id}")
        message_lines.append(f"<b>Cooler ID:</b> {Cooler_Id}")
        message_lines.append(f"<b>Fan ID:</b> {Fan_Id}")

    elif item_type == "Laptop":
        (
            Laptop_Id, Title, CPU_Id, GPU_Id, RAM_Id, SSD_Id, HDD_Id, Motherboard_Id,
            Battery_Id, Keyboard_Id, Touchpad_Id, Display_Id, Charger_Id, Webcam_Id,
            Case_Panel_Id, Photo_URL, Description, Notes_field, Condition, Created_At
        ) = item

        message_lines.append(f"<b>Condition:</b> {Condition}")
        message_lines.append(f"<b>CPU ID:</b> {CPU_Id}")
        message_lines.append(f"<b>GPU ID:</b> {GPU_Id}")
        message_lines.append(f"<b>RAM ID:</b> {RAM_Id}")
        message_lines.append(f"<b>Storage SSD ID:</b> {SSD_Id}")
        message_lines.append(f"<b>Storage HDD ID:</b> {HDD_Id}")
        message_lines.append(f"<b>Motherboard ID:</b> {Motherboard_Id}")
        message_lines.append(f"<b>Battery ID:</b> {Battery_Id}")
        message_lines.append(f"<b>Keyboard ID:</b> {Keyboard_Id}")
        message_lines.append(f"<b>Touchpad ID:</b> {Touchpad_Id}")
        message_lines.append(f"<b>Display ID:</b> {Display_Id}")
        message_lines.append(f"<b>Charger ID:</b> {Charger_Id}")
        message_lines.append(f"<b>Webcam ID:</b> {Webcam_Id}")
        message_lines.append(f"<b>Case Panel ID:</b> {Case_Panel_Id}")

    elif item_type == "Part":
        # For parts, just show name / type / condition if available
        (
            Part_Id, Title, Part_Type, Condition, Listed_Price,
            Bought_Price, Link, Contact_Info, Created_At
        ) = item

        message_lines.append(f"<b>Condition:</b> {Condition}")
        message_lines.append(f"<b>Part Type:</b> {Part_Type}")
        message_lines.append(f"<b>Link:</b> {Link or '-'}")
        message_lines.append(f"<b>Contact Info:</b> {Contact_Info or '-'}")
        message_lines.append(f"💰 <b>Added Price:</b> ${added_price}")

    return "\n".join(message_lines)
