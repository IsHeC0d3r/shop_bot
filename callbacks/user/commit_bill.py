from aiogram import Bot
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, update
from database.models.User import User
from database.models.AnyPay import AnyPay

from keyboards.builder import simple_keyboard_builder, Mode

from loader import anypay_api, admin_tag

async def commit_bill(callback: CallbackQuery, bot: Bot, db: AsyncSession) -> None:
    id = int(callback.data.split('_')[2])
    payments = anypay_api.get_payments(project_id=1)
    isSuccessful = False
    for payment in payments:
        if payment.id == id and payment.status == 'paid':
            data = await db.execute(select(AnyPay.amount, AnyPay.status).where(
                    (AnyPay.telegram == callback.message.chat.id) &
                    (AnyPay.transaction_id == id)
                )
            )
            data = data.all()[0]
            if data[1] == 0:
                await db.execute(update(AnyPay).where(
                        (AnyPay.telegram == callback.message.chat.id) &
                        (AnyPay.transaction_id == id)
                    ).values(status = 1)
                )
                await db.execute(update(User).where(
                        User.telegram == callback.message.chat.id
                    ).values(amount = User.amount + data[1], total_payed_amount = User.total_payed_amount + data[1])
                )
                isSuccessful = True
                break
    if isSuccessful:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=f'😎 <b>Сумма была успешно зачислена на ваш баланс.</b>\n\n'
            '<i>Приятных покупок!</i>',
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
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=f'❗️ <b>Оплата не была обнаружена! Пожалуйста, повторите попытку, либо свяжитесь с <a href="{admin_tag}"администратором</a></b>',
            reply_markup=simple_keyboard_builder(
                [
                    [
                        ['❌ Закрыть', 'back']
                    ]
                ],
                Mode.INLINE
            )
        )