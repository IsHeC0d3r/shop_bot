from aiogram import Bot
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from states.AdminStates import AdminState

from keyboards.builder import simple_keyboard_builder, Mode

async def add_category(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await state.set_state(AdminState.add_category)

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f'⏳ <b>Введите название категории</b>\n'
        '☝️ <b>Название должно быть не длиннее 50 символов.</b>\n\n',
        reply_markup=simple_keyboard_builder(
            [
                [
                    ['❌ Отмена', 'cancel']
                ]
            ],
            Mode.INLINE
        )
    )