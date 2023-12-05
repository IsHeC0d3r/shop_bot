from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from database.models.Cart import Cart

from keyboards.builder import simple_keyboard_builder, Mode
from misc.misc import pagination

from states.UserStates import UserState

async def cart(callback: CallbackQuery, bot: Bot, db: AsyncSession) -> None:
    cart = await db.execute(select(Cart.name, Cart.id).where(Cart.telegram == callback.message.chat.id))

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f'<b>👇 Твоя корзина</b>',
        reply_markup=simple_keyboard_builder(
            pagination(
                page=int(callback.data.split('cart_')[1]),
                data=cart.all(),
                callback_data='cart_product',
                callback_data_page='cart'
            ) + [*[[['🔙 Назад', 'back_profile'], ['✅ Оплатить', 'make_purchase']]]],
            Mode.INLINE
        )
    )

async def to_cart(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = callback.data.split('_')
    if int(data[4]) > 0:
        await state.set_state(UserState.input_products_count)
        await state.set_data({'category': data[2], 'product': data[3], 'available_count': data[4]})
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=f'<b>Введите количество.</b>\n'
            f'🔢 В наличии <b>{data[4]}</b> шт.',
            reply_markup=simple_keyboard_builder(
                [
                    [
                        ['❌ Отмена', 'cancel']
                    ]
                ],
                Mode.INLINE
            )
        )
    else:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=f'😔 <b>Похоже, что этого товара нет в наличии на данный момент.</b>\n\n'
            f'<i>Пожалуйста, попробуйте позже.</i>',
            reply_markup=simple_keyboard_builder(
                [
                    [
                        ['Назад', f'back_product_{data[2]}_{data[3]}']
                    ]
                ],
                Mode.INLINE
            )
        )