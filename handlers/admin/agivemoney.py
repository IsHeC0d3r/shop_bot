from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, update

from database.models.User import User

from misc.misc import format_text_to_amount, format_amount_to_text

async def agivemoney(msg: Message, db: AsyncSession, state: FSMContext) -> None:
    user_id = await state.get_data()
    user_id = user_id['user']
    amount = format_text_to_amount(msg.text)
    await db.execute(update(User).where(
            User.telegram == user_id
        ).values(balance = User.balance + amount))
    user = await db.execute(select(User.name, User.username, User.balance).where(User.telegram == user_id))
    user = user.all()[0]
    await msg.answer(
        text='😎 <b>Сумма была успешно зачислена на баланс пользователю.</b>\n\n'
        f'💲 Теперь у него на руках <b>{format_amount_to_text(user[2])}</b>₽'
    )
    await state.clear()