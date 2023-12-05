from aiogram import Bot
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from database.models.User import User
from database.models.Product import Product

from keyboards.builder import simple_keyboard_builder, Mode
from misc.misc import format_amount_to_text

async def product(callback: CallbackQuery, bot: Bot, db: AsyncSession) -> None:
    data = callback.data.split('_')
    product = await db.scalar(select(Product).where((Product.category == int(data[1])) & (Product.id == int(data[2]))))
    isAdmin = await db.execute(select(User.admin_lvl).where(User.telegram == callback.message.chat.id))
    isAdmin = isAdmin.all()[0]

    text=f'<b>{product.name}</b>\n\n' \
        f'💸 Цена: <b>{format_amount_to_text(product.price)}</b>₽\n' \
        f'🔢 В наличии: <b>{product.count}</b> шт.\n' \
        f'ℹ️ Описание: <b>{product.description}</b>\n'
    if isAdmin:
        kb = simple_keyboard_builder(
            [
                [
                    ['🧺 В корзину', f'to_cart_{data[1]}_{data[2]}_{product.count}']
                ],
                [
                    ['💰 Изменить цену', f'change_price_{data[1]}_{data[2]}'],
                    ['💰 Изменить количество', f'change_count_{data[1]}_{data[2]}']
                ],
                [
                    ['➖ Удалить', f'delete_product_{data[1]}_{data[2]}'],
                    ['🔙 Назад', f'back_category_{data[1]}_0']
                ]
            ],
            Mode.INLINE
        )
    else:
        kb = simple_keyboard_builder(
            [
                [
                    ['🔙 Назад', f'back_category_{data[1]}_0'],
                    ['🧺 В корзину', f'to_cart_{data[1]}_{data[2]}_{product.count}']
                ]
            ],
            Mode.INLINE
        )

    try:
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=product.photo,
            caption=f'<b>{product.name}</b>\n\n'
            f'💸 Цена: <b>{product.price}</b>₽\n'
            f'🔢 В наличии: <b>{product.count}</b> шт.\n'
            f'ℹ️ Описание: <b>{product.description}</b>\n',
            reply_markup=kb
        )
        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
    except:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=text,
            reply_markup=kb
        )