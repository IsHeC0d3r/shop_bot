from aiogram import Bot
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from database.models.User import User
from database.models.Category import Category

from keyboards.builder import simple_keyboard_builder, Mode
from misc.misc import pagination

async def categories(callback: CallbackQuery, bot: Bot, db: AsyncSession) -> None:
    categories = await db.execute(select(Category.name, Category.id))
    categories = categories.all()

    isAdmin = await db.execute(select(User.admin_lvl).where(User.telegram == callback.message.chat.id))
    isAdmin = isAdmin.all()[0]
    
    text = '<b>👇 Список категорий</b>'
    
    kb_list = simple_keyboard_builder(
        pagination(
            page=int(callback.data.split('categories_')[1]),
            data=categories,
            callback_data='category_%%_0',
            callback_data_page=f'categories'
        ) + [*[[['➕ Добавить категорию', f'add_category']], [['❌ Закрыть', 'back']]]] if isAdmin else [*[[['❌ Закрыть', 'back']]]],
        Mode.INLINE
    )

    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=text,
            reply_markup=kb_list
        )
    except:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=kb_list
        )