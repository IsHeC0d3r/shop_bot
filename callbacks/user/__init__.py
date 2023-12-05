from aiogram import Dispatcher, F

from .back import back, cancel, skip

from .categories import categories
from .products import products
from .product import product
from .cart_product import cart_product, cart_remove
from .cart import cart, to_cart
from .make_purchase import make_purchase
from .put_money import put_money
from .commit_bill import commit_bill

async def init(dp: Dispatcher) -> None:
    dp.callback_query.register(back, F.data.startswith('back'))
    dp.callback_query.register(cancel, F.data == 'cancel')
    dp.callback_query.register(skip, F.data == 'skip')

    dp.callback_query.register(categories, F.data.startswith('categories_'))
    dp.callback_query.register(products, F.data.startswith('category_'))
    dp.callback_query.register(product, F.data.startswith('product_'))

    dp.callback_query.register(cart_product, F.data.startswith('cart_product_'))
    dp.callback_query.register(cart_remove, F.data.startswith('cart_remove_'))
    dp.callback_query.register(cart, F.data.startswith('cart_'))
    dp.callback_query.register(to_cart, F.data.startswith('to_cart_'))

    dp.callback_query.register(make_purchase, F.data == 'make_purchase')
    dp.callback_query.register(put_money, F.data == 'put_money')
    dp.callback_query.register(commit_bill, F.data.startswith('commit_bill_'))