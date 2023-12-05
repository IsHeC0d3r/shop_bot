from aiogram.fsm.state import StatesGroup, State

class AdminState(StatesGroup):
    givemoney = State()

    add_category = State()

    add_product_info = State()
    add_product_photo = State()

    change_price = State()
    change_count = State()
    delete_product = State()

    alert_user = State()