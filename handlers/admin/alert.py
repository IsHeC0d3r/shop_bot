from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from database.models.User import User

from aiogram.exceptions import TelegramForbiddenError

async def alert_user(msg: Message, db: AsyncSession, state: FSMContext, bot: Bot) -> None:
    user = await state.get_data()
    text = f'🥳 <b>Сообщение было успешно отправлено пользователю <a href="t.me/{user["username"]}">{user["name"]}</a></b>'
    try:
        await bot.send_message(
            chat_id=user['id'],
            text=msg.text
        )
    except TelegramForbiddenError:
        text = f'😔<b>Сообщение не доставлено пользователю <a href="t.me/{user["username"]}">{user["name"]}</a></b>\n\n' \
            '💁 <i>Причина: пользователь заблокировал бота</i>'
    except:
        text = f'😔<b>Сообщение не доставлено пользователю <a href="t.me/{user["username"]}">{user["name"]}</a></b>\n\n' \
            '💁 <i>Причина: не обрабатываемая ошибка. Пожалуйста, обратитесь к разработчику бота, если это будет повторяться на постоянной основе.</i>'
    await msg.answer(text)
    await state.clear()

async def alert(msg: Message, db: AsyncSession, command: CommandObject, bot: Bot) -> None:
    if command.args:
        users = await db.scalars(select(User))
        users = users.all()

        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.telegram,
                    text=command.args
                )
            except:#Exception as e:
                #print(e)
                pass
    else:
        await msg.answer(
            text='❗️ *Не правильно использована команда\.*\n'
            '*Пример:* /alert \<b\>test alert for all users\</b\>',
            parse_mode='MarkdownV2'
        )