from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, delete
from database.models.Cart import Cart
from database.models.Product import Product

from keyboards.builder import simple_keyboard_builder, Mode

from misc.misc import format_amount_to_text

from callbacks.user.cart import cart

async def cart_product(callback: CallbackQuery, bot: Bot, db: AsyncSession) -> None:
    data = callback.data.split('_')
    cart = await db.execute(select(Cart.category_id, Cart.product_id, Cart.count).where(Cart.id == int(data[2])))
    cart = cart.all()[0]
    product = await db.scalar(select(Product).where((Product.category == int(cart[0])) & (Product.id == int(cart[1]))))
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f'<b>{product.name}</b>\n\n'
        f'💸 Цена: <b>{format_amount_to_text(product.price)}</b>₽\n'
        f'🔢 В наличии: <b>{product.count}</b> шт.\n'
        f'🔢 Выбранное количество: <b>{cart[2]}</b> шт.\n'
        f'ℹ️ Описание: <b>{product.description}</b>\n',
        reply_markup=simple_keyboard_builder(
            [
                [
                    ['🔙 Назад', f'back_cart_0'],
                    ['🗑 Удалить', f'cart_remove_{data[2]}']
                ]
            ],
            Mode.INLINE
        )
    )

async def cart_remove(callback: CallbackQuery, bot: Bot, db: AsyncSession, state: FSMContext):
    data = callback.data.split('_')
    await db.execute(delete(Cart).where(Cart.id == int(data[2])))
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=f'<b>Товар успешно удален из корзины.</b>\n'
    )
    await cart(
        callback=CallbackQuery(
            id=callback.id,
            from_user=callback.from_user,
            chat_instance=callback.chat_instance,
            message=callback.message,
            data='cart_0'
        ),
        bot=bot,
        db=db
    )