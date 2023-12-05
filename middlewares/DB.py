from typing import Any, Awaitable, Callable, Dict, Optional, Set
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update, Message, CallbackQuery

from loader import db

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, update
from database.models.User import User

class DB(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		event: Update,
		data: Dict[str, Any]
	) -> Any:
		async with db.session() as session:
			data['db']: AsyncSession = session
		async def update_data(id, name, username):
			user = await data['db'].execute(select(User.name, User.username).where(User.telegram == id))
			user = user.all()
			if user:
				user = user[0]
				if name != user[0] or username != user[1]:
					await data['db'].execute(update(User).where(User.telegram == id).values(
						name = name,
						username = username
					))
		if(isinstance(event, Message)):
			full_name = event.chat.first_name; full_name = f'{full_name} {event.chat.last_name}' if event.from_user.last_name else full_name
			await update_data(event.chat.id, full_name, event.chat.username)
		if(isinstance(event, CallbackQuery)):
			full_name = event.message.chat.first_name; full_name = f'{full_name} {event.message.chat.last_name}' if event.from_user.last_name else full_name
			await update_data(event.message.chat.id, full_name, event.message.chat.username)
		handler = await handler(event, data)
		if data['db']:
			await data['db'].commit()
			await data['db'].close()
			del data['db']
		return handler
	
	def setup(
		self: BaseMiddleware, router: Dispatcher, exclude: Optional[Set[str]] = None
	) -> BaseMiddleware:
		"""
		Register middleware for all events in the Router

		:param router:
		:param exclude:
		:return:
		"""
		if exclude is None:
			exclude = set()
		exclude_events = {"update", *exclude}
		for event_name, observer in router.observers.items():
			if event_name in exclude_events:
				continue
			observer.outer_middleware(self)
		return self