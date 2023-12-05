from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, update
from database.models.Cart import Cart
from database.models.Product import Product

from keyboards.builder import simple_keyboard_builder, Mode

async def to_cart(msg: Message, db: AsyncSession, state: FSMContext) -> None:
    data = await state.get_data()
    if int(data['available_count']) >= int(msg.text):
        product = await db.execute(select(Product.name, Product.price).where((Product.category == int(data['category'])) & (Product.id == int(data['product']))))
        product = product.all()[0]
        if await db.scalar(select(Cart).where((Cart.category_id == int(data['category'])) & (Cart.product_id == int(data['product'])))):
            await db.execute(
                update(Cart).where((Cart.category_id == int(data['category'])) &
                    (Cart.product_id == int(data['product']))).values(
                        count = Cart.count + int(msg.text)
                    )
                )
        else:
            db.add(
                Cart(
                    telegram = msg.chat.id,
                    category_id = int(data['category']),
                    product_id = int(data['product']),
                    name = product[0],
                    count = int(msg.text),
                    price = product[1]
                )
            )
        await msg.answer(
            text='❗️ <b>Товар успешно добавлен в корзину.</b>\n\n',
            reply_markup=simple_keyboard_builder(
                [
                    [
                        ['❌ Закрыть', 'back']
                    ]
                ],
                Mode.INLINE
            )
        )
    else:
        await msg.answer(
            text='❗️ <b>Произошла ошибка</b>\n\n'
            f'🔢 Текущее количество товара в наличии - <b>{data["available_count"]}</b> шт.\n'
            f'🔢 Введенное количество - <b>{msg.text}</b> шт.\n\n'
            'Проверьте правильность введённых данных и попробуйте снова.',
            reply_markup=simple_keyboard_builder(
                [
                    [
                        ['❌ Отмена', 'cancel']
                    ]
                ],
                Mode.INLINE
            )
        )
        return
    await state.clear()