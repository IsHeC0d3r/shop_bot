from aiogram import Dispatcher, F
from aiogram.filters.command import Command

from .start import start

from .profile import profile
from .categories import categories
from .call_admin import call_admin

from states.UserStates import UserState
from .put_money import put_money
from .to_cart import to_cart

async def init(dp: Dispatcher) -> None:
    dp.message.register(start, Command('start'))

    dp.message.register(profile, F.text == '🧍 Профиль')
    dp.message.register(categories, F.text == '🛍 Товары')
    dp.message.register(call_admin, F.text == '🔗 Обратная связь')

    dp.message.register(put_money, UserState.input_amount)
    dp.message.register(to_cart, UserState.input_products_count)