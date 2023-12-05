from aiogram import Bot
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from database.models.User import User
from database.models.Purchase import Purchase

from keyboards.builder import simple_keyboard_builder, Mode
from misc.misc import pagination, format_amount_to_text

async def apurchases(callback: CallbackQuery, db: AsyncSession, bot: Bot) -> None:
    data = callback.data.split('_')

    purchases = await db.execute(select(Purchase.product_name, Purchase.id).where(Purchase.telegram == int(data[1])))
    user = await db.execute(select(User.name, User.username).where(User.telegram == int(data[1])))
    user = user.all()[0]

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f'<b>👇 Покупки пользователя <a href="t.me/{user.username}">{user.name}</a></b>',
        reply_markup=simple_keyboard_builder(
            pagination(
                page=int(data[2]),
                data=purchases.all(),
                callback_data=f'apurchase_{data[1]}',
                callback_data_page=f'{data[0]}_{data[1]}'
            ) + [*[[['🔙 Назад', f'back_aprofile_{data[1]}']]]],
            Mode.INLINE
        )
    )

async def apurchase(callback: CallbackQuery, db: AsyncSession, bot: Bot) -> None:
    data = callback.data.split('_')
    purchase = await db.scalar(select(Purchase).where(Purchase.id == int(data[2])))
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f'<b>{purchase.product_name}</b>\n\n' \
        f'💸 Цена (за штуку): <b>{format_amount_to_text(purchase.product_price)}</b>₽\n' \
        f'🔢 Куплено: <b>{purchase.product_count}</b> шт.\n' \
        f'💸 Суммарно потрачено: <b>{format_amount_to_text(purchase.product_price * purchase.product_count)}</b>₽\n',
        reply_markup=simple_keyboard_builder(
            [
                [
                    ['🔙 Назад', f'back_apurchases_{data[1]}_0']
                ]
            ],
            Mode.INLINE
        )
    )