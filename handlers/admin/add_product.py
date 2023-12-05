from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import update
from aiogram.fsm.context import FSMContext

from database.models.Product import Product

from keyboards.builder import simple_keyboard_builder, Mode

from misc.misc import format_text_to_amount, is_int64

from states.AdminStates import AdminState

async def add_product_info(msg: Message, db: AsyncSession, state: FSMContext) -> None:
    product_info = msg.text.split('\n')
    if len(product_info) == 4:
        if len(product_info[0]) <= 50:
            if len(product_info[1]) <= 250:
                if format_text_to_amount(product_info[2]):
                    if is_int64(product_info[3]):
                        if(int(product_info[3])) > 0:
                            state_data = await state.get_data()
                            product = Product(
                                category = int(state_data['category']),
                                name = product_info[0],
                                description = product_info[1],
                                price = format_text_to_amount(product_info[2]),
                                count = int(product_info[3])
                            )
                            db.add(
                                product
                            )
                            await db.commit()
                            await state.clear()
                            await state.set_data({'id': product.id})
                            await state.set_state(AdminState.add_product_photo)
                            await msg.answer(
                                text='<b>Отправьте боту изображение для товара или нажмите "❌ Пропустить"</b>.',
                                reply_markup=simple_keyboard_builder(
                                    [
                                        [
                                            ['❌ Пропустить', 'skip']
                                        ]
                                    ],
                                    Mode.INLINE
                                )
                            )
                        else:
                            await msg.answer(
                                text='❗️ <b>Количество товара не должно быть меньше одного.</b>\n\n'
                                '☝️ Пожалуйста, проверьте правильность введённых данных и повторите попытку.'
                            )
                    else:
                        await msg.answer(
                            text='❗️ <b>Количество товара слишком большое.</b>\n\n'
                            '☝️ Пожалуйста, проверьте правильность введённых данных и повторите попытку.'
                        )
                else:
                    await msg.answer(
                        text='❗️ <b>Не верный формат цены.</b>\n\n'
                        '☝️ Пожалуйста, проверьте правильность введённых данных и повторите попытку.'
                    )
            else:
                await msg.answer(
                    text='❗️ <b>Количество символов в описании не должно превышать 250 символов.</b>\n\n'
                    '☝️ Пожалуйста, проверьте правильность введённых данных и повторите попытку.'
                )
        else:
            await msg.answer(
                text='❗️ <b>Количество символов в названии не должно превышать 50 символов.</b>\n\n'
                '☝️ Пожалуйста, проверьте правильность введённых данных и повторите попытку.'
            )
    else:
        await msg.answer(
                text='❗️ <b>Пожалуйста, ознакомьтесь с примером и повторите попытку.</b>'
            )
    # db.add(
    #     Category(
    #         name = msg.text
    #     )
    # )
    # await msg.answer(
    #     text=f'<b>Категория "{msg.text}" была успешно создана!</b>'
    # )

async def add_product_photo(msg: Message, db: AsyncSession, state: FSMContext) -> None:
    state_data = await state.get_data()
    id = state_data['id']
    await db.execute(update(Product).where(
            Product.id == int(id)
        ).values(
            photo = msg.photo[-1].file_id
        )
    )
    await msg.answer(
        text=f'<b>Фотография была успешно установлена!</b>'
    )
    await state.clear()