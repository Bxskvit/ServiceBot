from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.buttons_ikb import BUTTONS


def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Initializing bot
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Initializing buttons' list
    buttons: list[InlineKeyboardButton] = []

    # completing list(*args and **kwargs)
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=BUTTONS[button] if button in BUTTONS else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # unpacking buttons' list by method 'row' and with argument 'width'
    kb_builder.row(*buttons, width=width)

    # returning inline keyboard object
    return kb_builder.as_markup()
