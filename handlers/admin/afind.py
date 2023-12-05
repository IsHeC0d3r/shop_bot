from aiogram.types import Message
from aiogram.filters import CommandObject

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from database.models.User import User
from database.models.Purchase import Purchase

from keyboards.builder import simple_keyboard_builder, Mode
from misc.misc import format_amount_to_text, TimeDifference
from datetime import datetime

async def afind(msg: Message, command: CommandObject, db: AsyncSession) -> None:
    if command.args and len(command.args.split(' ')) == 1:
        user = None
        if command.args.startswith('@'):
            user: User = await db.scalar(select(User).where(User.username == command.args[1:]))
        else:
            user: User = await db.scalar(select(User).where(User.telegram == int(command.args)))
        if user:
            purchases = await db.scalars(select(Purchase.id).where(Purchase.telegram == user.telegram))
            purchases = len(purchases.all())


            await msg.answer(
                text=f'👤 <b>Профиль пользователя</b> <a href="t.me/{user.username}">{user.name}</a>\n\n'
                f'🆔 <b>ID: {user.telegram}</b>\n'
                f'👤 <b>Логин:</b> @{user.username}\n'
                f'👤 <b>Имя:</b> <a href="t.me/{user.username}">{user.name}</a>\n'
                f'🕰 Регистрация: <b>{user.time.strftime("%d-%m-%Y %H:%M:%S")}</b> ({TimeDifference(start=user.time, end=datetime.now()).get_difference(withHTML=True)})\n\n'
                f'💰 Баланс: <b>{format_amount_to_text(user.balance)}</b>₽\n'
                f'💸 Всего пополнено: <b>{format_amount_to_text(user.total_payed_amount)}</b>₽\n'
                f'🎁 Куплено товаров: <b>{purchases}</b> шт.',
                reply_markup=simple_keyboard_builder(
                    [
                        [
                            ['🎁 Покупки', f'apurchases_{user.telegram}_0'], ['💰 Выдать баланс', f'agivemoney_{user.telegram}']
                        ],
                        [
                            ['💌 Отправить СМС', f'alert_user_{user.telegram}']
                        ],
                        [
                            ['❌ Закрыть', 'back']
                        ]
                    ],
                    Mode.INLINE
                )
            )
        else:
            await msg.answer(
                text='❗️ Такого пользователя нет в базе.'
            )
    else:
        await msg.answer(
            text='❗️ <b>Не правильно использована команда.</b>\n'
            '<b>Пример:</b> /afind @durov; /afind 123'
        )