from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from database.models.User import User
from database.models.Purchase import Purchase
from database.models.Cart import Cart

from keyboards.builder import simple_keyboard_builder, Mode
from misc.misc import format_amount_to_text

async def profile(msg: Message, db: AsyncSession) -> None:
    user = await db.scalar(select(User).where(User.telegram == msg.chat.id))
    purchases = await db.scalars(select(Purchase.product_price).where(Purchase.telegram == msg.chat.id))
    cart = await db.scalars(select(Cart.id).where(Cart.telegram == msg.chat.id))

    purchases = len(purchases.all())
    cart = len(cart.all())
    
    await msg.answer(
        text='🧍 Твой профиль:\n\n'
            f'    💰 Баланс - <b>{format_amount_to_text(user.balance)}</b>₽\n'
            f'    🥇 Количество покупок - <b>{purchases}</b> шт.\n'
            f'    💷 Количество товаров в корзине - <b>{cart}</b> шт.',
        reply_markup=simple_keyboard_builder(
            [
                [
                    ['🧺 Корзина', 'cart_0'], ['💸 Пополнить баланс', 'put_money']
                ],
                [
                    ['❌ Закрыть', 'back']
                ]
            ],
            Mode.INLINE
        )
    )