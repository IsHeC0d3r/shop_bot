from aiogram.fsm.state import StatesGroup, State

class UserState(StatesGroup):
    input_amount = State()
    input_products_count = State()