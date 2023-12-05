from typing import Any, Awaitable, Callable, Dict, Optional, Set
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update

class CallbackFix(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		event: Update,
		data: Dict[str, Any]
	) -> Any:
		await event.answer('')
		return await handler(event, data)