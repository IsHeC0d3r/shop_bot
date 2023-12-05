from aiogram import Bot
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from states.AdminStates import AdminState

from keyboards.builder import simple_keyboard_builder, Mode

async def change_price(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    data = callback.data.split('_')
    await state.set_state(AdminState.change_price)
    await state.set_data({
        'category': data[2],
        'id': data[3],
    })
    text = f'⏳ <b>Введите новую цену</b>\n' \
        '💁 <i>Пример: 100.21; 100,21; 100</i>'
    kb = simple_keyboard_builder(
        [
            [
                ['❌ Отмена', 'cancel']
            ]
        ],
        Mode.INLINE
    )
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=text,
            reply_markup=kb
        )
    except:
        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=kb
        )