
def format_computer_description_message(computer: tuple) -> str:
    """
    Takes a single computer row as a tuple and returns a nicely formatted message.
    Column order must match your CREATE TABLE order.
    """
    (
        Post_id, Title, Description, Type, CPU, CPU_Fan, Motherboard, GPU,
        RAM, Storage, PSU, PC_Case, Screen_Size, Display_Type, OS,
        Connectivity, Ports, Weight, Battery, Price, Best_Usage,
        Additional_Info, Post_Date
    ) = computer

    message = f"<b>{Title}</b>\n"

    if Description:
        message += f"{Description}\n\n"

    message += f"<b>Type:</b> {Type}\n"
    message += f"<b>CPU:</b> {CPU}\n"
    message += f"<b>CPU Fan:</b> {CPU_Fan or '-'}\n"
    message += f"<b>Motherboard:</b> {Motherboard or '-'}\n"
    message += f"<b>GPU:</b> {GPU or '-'}\n"
    message += f"<b>RAM:</b> {RAM or '-'}\n"
    message += f"<b>Storage:</b> {Storage or '-'}\n"
    message += f"<b>PSU:</b> {PSU or '-'}\n"
    message += f"<b>Case:</b> {PC_Case or '-'}\n"

    if Screen_Size or Display_Type:
        message += f"<b>Display:</b> {Screen_Size or '-'}{'\"' if Screen_Size else ''} {Display_Type or ''}\n"

    message += f"<b>OS:</b> {OS or '-'}\n"
    message += f"<b>Connectivity:</b> {Connectivity or '-'}\n"
    message += f"<b>Ports:</b> {Ports or '-'}\n"
    message += f"<b>Weight:</b> {Weight or '-'}\n"
    message += f"<b>Battery:</b> {Battery or '-'}\n"
    message += f"<b>Best Usage:</b> {Best_Usage or '-'}\n"

    if Additional_Info:
        message += f"<b>Additional Info:</b> {Additional_Info}\n"

    message += f"\n💰 <b>Price:</b> ${Price}\n"
    message += f"<i>Posted on: {Post_Date}</i>"

    return message
