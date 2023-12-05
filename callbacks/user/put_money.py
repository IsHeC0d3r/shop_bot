from aiogram import Bot
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from states.UserStates import UserState

from keyboards.builder import simple_keyboard_builder, Mode

async def put_money(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text='<b>Введите сумму для пополнения</b>\n\n'
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
    await state.set_state(UserState.input_amount)