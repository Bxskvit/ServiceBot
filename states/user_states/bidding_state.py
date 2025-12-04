from aiogram.fsm.state import State, StatesGroup


class BidState(StatesGroup):
    waiting_for_price = State()
