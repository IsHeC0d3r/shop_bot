from aiogram import Bot
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from states.AdminStates import AdminState

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, delete
from database.models.Product import Product
from database.models.Cart import Cart

async def delete_product(callback: CallbackQuery, db: AsyncSession, bot: Bot) -> None:
    data = callback.data.split('_')
    await db.execute(delete(Product).where(
        (Product.category == int(data[2])) &
        (Product.id == int(data[3]))
    ))
    await db.execute(delete(Cart).where(
        (Cart.category_id == int(data[2])) &
        (Cart.product_id == int(data[3]))
    ))
    text = f'✅ <b>Товар был успешно удален.</b>'
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=text
        )
    except:
        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text
        )