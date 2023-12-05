from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from database.models.User import User
from keyboards.reply import kb_start

async def start(msg: Message, db: AsyncSession) -> None:
	user = await db.scalar(select(User).where(User.telegram == msg.chat.id))
	if user:
		await msg.answer(
			text='🙋 <b>Рад видеть тебя снова!</b>\n\n'
			'👇 <i>Выбери нужную кнопку в меню ниже</i>',
			reply_markup=kb_start
		)
	else:
		await msg.answer(
			text=f'🙋 <b>Добро пожаловать, {msg.from_user.first_name}!</b>\n\n'
			'👇 <i>Выбери нужную кнопку в меню ниже</i>',
			reply_markup=kb_start
		)
		full_name = msg.chat.first_name; full_name = f'{full_name} {msg.chat.last_name}' if msg.from_user.last_name else full_name
		db.add(
			User(
				telegram = msg.chat.id,
				name = full_name,
				username = msg.from_user.username
			)
		)