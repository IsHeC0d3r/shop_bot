from aiogram import Bot
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from states.AdminStates import AdminState

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from database.models.User import User

from keyboards.builder import simple_keyboard_builder, Mode

async def alert_user(callback: CallbackQuery, db: AsyncSession, bot: Bot, state: FSMContext) -> None:
    user_id = int(callback.data.split('_')[2])

    user = await db.execute(select(User.name, User.username).where(User.telegram == user_id))
    user = user.all()[0]

    await state.update_data(
        id=user_id,
        name=user[0],
        username=user[1]
    )
    await state.set_state(AdminState.alert_user)

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f'⏳ <b>Введите сообщение, которое хотите отправить пользователю <a href="t.me/{user.username}">{user.name}</a></b>\n',
        reply_markup=simple_keyboard_builder(
            [
                [
                    ['❌ Отмена', 'cancel']
                ]
            ],
            Mode.INLINE
        )
    )