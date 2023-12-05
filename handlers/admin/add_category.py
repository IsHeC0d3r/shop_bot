from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, update
from aiogram.fsm.context import FSMContext

from database.models.Category import Category

async def add_category(msg: Message, db: AsyncSession, state: FSMContext) -> None:
    await state.clear()
    db.add(
        Category(
            name = msg.text
        )
    )
    await msg.answer(
        text=f'<b>Категория "{msg.text}" была успешно создана!</b>'
    )