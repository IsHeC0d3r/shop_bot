from aiogram.types import Message
from aiogram.filters import CommandObject

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, update

from database.models.User import User

async def make_admin(msg: Message, command: CommandObject, db: AsyncSession) -> None:
    if command.args and len(command.args.split(' ')) == 1:
        user = None
        if command.args.startswith('@'):
            user: User = await db.scalar(select(User).where(User.username == command.args[1:]))
        else:
            user: User = await db.scalar(select(User).where(User.telegram == int(command.args)))
        if user:
            await db.execute(update(User).where(
                User.id == user.id
            ).values(admin_lvl = 1))


            await msg.answer(
                text=f'🥳 <b>Пользователь</b> <a href="t.me/{user.username}">{user.name}</a> успешно повышен до администратора\n\n',
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