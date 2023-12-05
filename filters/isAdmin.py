from aiogram.filters import BaseFilter
from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from database.models.User import User

class AdminFilter(BaseFilter):
    async def __call__(self, msg: Message, db: AsyncSession) -> bool:
        isAdmin = await db.scalar(select(User.admin_lvl).where(
                User.telegram == msg.chat.id
            )
        )

        return isAdmin