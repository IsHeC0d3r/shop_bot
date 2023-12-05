from aiogram import Bot
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from database.models.User import User
from database.models.Product import Product

from keyboards.builder import simple_keyboard_builder, Mode
from misc.misc import pagination, format_amount_to_text

async def products(callback: CallbackQuery, bot: Bot, db: AsyncSession) -> None:
    data = callback.data.split('_')
    isAdmin = await db.execute(select(User.admin_lvl).where(User.telegram == callback.message.chat.id))
    isAdmin = isAdmin.all()[0]
    products = await db.execute(select(Product.name, Product.price, Product.id).where(Product.category == int(data[1])))
    products = products.all()
    output = [(f'{i[0]} | {format_amount_to_text(i[1])}₽', i[2]) for i in products]

    text = f'<b>👇 Список товаров в данной категории</b>'
    kb = simple_keyboard_builder(
        pagination(
            page=int(data[2]),
            data=output,
            callback_data=f'product_{data[1]}',
            callback_data_page=f'category_{data[1]}'
        ) + [*[[['➕ Добавить товар', f'add_product_{data[1]}'], ['➖ Удалить категорию', f'delete_category_{data[1]}']], [['🔙 Назад', 'back_categories_0']]]] if isAdmin else [*[[['🔙 Назад', 'back_categories_0']]]],
        Mode.INLINE
    )
    
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=text,
            reply_markup=kb
        )
    except:
        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=kb
        )