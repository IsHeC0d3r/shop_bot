from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import update

from database.models.Product import Product

from misc.misc import format_text_to_amount

async def change_price(msg: Message, db: AsyncSession, state: FSMContext) -> None:
    data = await state.get_data()
    count = format_text_to_amount(msg.text)
    await db.execute(update(Product).where(
            (Product.category == int(data['category'])) &
            (Product.id == int(data['id']))
        ).values(count = int(count)))
    await msg.answer(
        text='😎 <b>Количество товара было успешно изменено.</b>\n\n'
        f'💲 Теперь оно стало <b>{count}</b>₽'
    )
    await state.clear()