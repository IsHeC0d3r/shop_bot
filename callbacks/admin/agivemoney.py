from aiogram import Bot
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from states.AdminStates import AdminState

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, update

from database.models.User import User

from keyboards.builder import simple_keyboard_builder, Mode

async def agivemoney(callback: CallbackQuery, db: AsyncSession, bot: Bot, state: FSMContext) -> None:
    user_id = int(callback.data.split('_')[1])
    await state.update_data(user=user_id)
    await state.set_state(AdminState.givemoney)

    user = await db.execute(select(User.name, User.username).where(User.telegram == user_id))
    user = user.all()[0]

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f'⏳ <b>Введите сумму, которую хотите зачислить пользователю <a href="t.me/{user.username}">{user.name}</a></b>\n'
        '☝️ <b>Вы так же можете отнимать деньги у пользователя, введя "-" перед цифрой.</b>\n\n'
        '💁 <i>Пример: 100.21; 100,21; 100</i>',
        reply_markup=simple_keyboard_builder(
            [
                [
                    ['❌ Отмена', 'cancel']
                ]
            ],
            Mode.INLINE
        )
    )