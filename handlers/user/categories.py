from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio.session import AsyncSession

from callbacks.user.categories import categories as c_categories

async def categories(msg: Message, db: AsyncSession, bot: Bot) -> None:
    await c_categories(
        callback=CallbackQuery(
            id='',
            from_user=msg.from_user,
            chat_instance='',
            message=msg,
            data='categories_0'
        ),
        bot=bot,
        db=db
    )
    # categories = await db.execute(select(Category.name, Category.id))
    # categories = categories.all()

    # await msg.answer(
    #     text=f'<b>👇 Список категорий</b>',
    #     reply_markup=simple_keyboard_builder(
    #         pagination(
    #             page=0,
    #             data=categories,
    #             callback_data='products_%%_0',
    #             callback_data_page='categories'
    #         ) + [*[[['❌ Закрыть', 'back']]]],
    #         Mode.INLINE
    #     )
    # )