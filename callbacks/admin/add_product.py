from aiogram import Bot
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from states.AdminStates import AdminState

from keyboards.builder import simple_keyboard_builder, Mode

async def add_product(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await state.set_data({'category':callback.data.split('_')[2]})
    await state.set_state(AdminState.add_product_info)

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f'⏳ <b>Введите информацию о товар в следующем формате:</b>\n\n'
        '<b>Название</b> (<b>50</b> символов максимум)\n'
        '<b>Описание</b> (<b>250</b> символов максимум)\n'
        '<b>Цена</b>\n'
        '<b>Количество</b>\n'
        '💁 <b>Пример:</b>\n'
        'Аккаунт VK муж.\n'
        'Аккаунт VK. Отлежка 3+ месяца. Подходит под спам.\n'
        '15.25\n'
        '50',
        reply_markup=simple_keyboard_builder(
            [
                [
                    ['❌ Отмена', 'cancel']
                ]
            ],
            Mode.INLINE
        )
    )