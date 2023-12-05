from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession
from database.models.AnyPay import AnyPay

from keyboards.builder import simple_keyboard_builder, Mode

from loader import anypay_api

from misc.misc import format_amount_to_text, format_text_to_amount

from random import randint

async def put_money(msg: Message, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
    amount = format_text_to_amount(msg.text)
    text_amount = format_amount_to_text(amount)
    bill = await anypay_api.create_payment(
        pay_id=randint(1,1111111111),
        method='qiwi',
        email='test@mail.ru',
        amount=print(float(text_amount)), 
        currency='RUB'
    )
    db.add(
        AnyPay(
            telegram = msg.chat.id,
            transaction_id = bill.id,
            amount = amount,
            status = 0
        )
    )
    await msg.answer(
        text='🙋 <b>Платёж был успешно создан!</b>\n\n'
        f'💳 Сумма - <b>{text_amount}</b>₽\n'
        f'✖️ ID Транзакции: <b>...</b>\n'
        f'✖️ ID Покупателя: <b>{msg.chat.id}</b>\n'
        f'💲 Валюта: <b>RUB</b>\n\n'
        '💁 <i>Подсказка: Для оплаты нажмите на кнопку "🔗 Оплатить" ниже и следуйте дальнейшим инструкциям. После оплаты нажмите кнопку "✅ Подтвердить оплату" и ожидайте получение товара.</i>',
        reply_markup=simple_keyboard_builder(
            [
                [
                    ['🔗 Оплатить', f'__url__{bill.url}']
                ],
                [
                    ['✅ Подтвердить оплату', f'commit_bill_{bill.transaction_id}']
                ]
            ],
            Mode.INLINE
        )
    )