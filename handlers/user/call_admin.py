from aiogram.types import Message

from loader import admin_tag

async def call_admin(msg: Message) -> None:
	await msg.answer(f'ℹ️ <b>Тег администратора для обратной связи: {admin_tag}.</b>')