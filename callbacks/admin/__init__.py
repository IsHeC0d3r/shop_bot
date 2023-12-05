from aiogram import Dispatcher, F

from .apurchases import apurchases, apurchase
from .agivemoney import agivemoney

from .add_category import add_category
from .add_product import add_product

from .delete_category import delete_category
from .delete_product import delete_product

from .change_price import change_price

from .alert_user import alert_user

async def init(dp: Dispatcher) -> None:
    dp.callback_query.register(apurchases, F.data.startswith('apurchases_'))
    dp.callback_query.register(apurchase, F.data.startswith('apurchase_'))
    dp.callback_query.register(agivemoney, F.data.startswith('agivemoney_'))

    dp.callback_query.register(add_category, F.data.startswith('add_category'))
    dp.callback_query.register(add_product, F.data.startswith('add_product_'))

    dp.callback_query.register(delete_category, F.data.startswith('delete_category'))
    dp.callback_query.register(delete_product, F.data.startswith('delete_product'))

    dp.callback_query.register(change_price, F.data.startswith('change_price_'))

    dp.callback_query.register(alert_user, F.data.startswith('alert_user_'))