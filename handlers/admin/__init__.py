from aiogram import Dispatcher, F
from aiogram.filters import Command
from filters.isAdmin import AdminFilter
from states.AdminStates import AdminState

from .afind import afind

from .agivemoney import agivemoney

from .add_category import add_category
from .add_product import add_product_info, add_product_photo

from .change_price import change_price

from .make_admin import make_admin

from .alert import alert_user, alert

async def init(dp: Dispatcher) -> None:
    dp.message.register(afind, Command('afind'), AdminFilter())
    
    dp.message.register(agivemoney, AdminState.givemoney, AdminFilter())
    
    dp.message.register(add_category, AdminState.add_category, AdminFilter())
    dp.message.register(add_product_info, AdminState.add_product_info, AdminFilter())
    dp.message.register(add_product_photo, F.photo, AdminState.add_product_photo, AdminFilter())

    dp.message.register(change_price, AdminState.change_price, AdminFilter())

    dp.message.register(make_admin, Command('makeadmin'), AdminFilter())

    dp.message.register(alert_user, AdminState.alert_user, AdminFilter())
    dp.message.register(alert, Command('alert'), AdminFilter())