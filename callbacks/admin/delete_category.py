from aiogram import Bot
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import delete
from database.models.Category import Category
from database.models.Cart import Cart

async def delete_category(callback: CallbackQuery, db: AsyncSession, bot: Bot) -> None:
    data = callback.data.split('_')
    await db.execute(delete(Category).where(
        Category.id == int(data[2])
    ))
    await db.execute(delete(Cart).where(
        Cart.category_id == int(data[2])
    ))
    text = f'✅ <b>Категория была успешно удалена.</b>'
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