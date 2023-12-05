from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, update

from database.models.User import User
from database.models.Product import Product
from database.models.Cart import Cart

from misc.misc import format_text_to_amount, format_amount_to_text

async def change_price(msg: Message, db: AsyncSession, state: FSMContext) -> None:
    data = await state.get_data()
    amount = format_text_to_amount(msg.text)
    await db.execute(update(Product).where(
            (Product.category == int(data['category'])) &
            (Product.id == int(data['id']))
        ).values(price = int(amount))
    )
    await db.execute(update(Cart).where(
            (Cart.category_id == int(data['category'])) &
            (Cart.product_id == int(data['id']))
        ).values(price = int(amount))
    )
    await msg.answer(
        text='😎 <b>Стоимость товара была успешно изменена.</b>\n\n'
        f'💲 Теперь он стоит <b>{format_amount_to_text(amount)}</b>₽'
    )
    await state.clear()