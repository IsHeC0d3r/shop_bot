from aiogram import Dispatcher

from .IncorrectInput import IncorrectInput
from .DB import DB
from .CallbackFix import CallbackFix

async def init(dp: Dispatcher) -> None:
	IncorrectInput().setup(router=dp)
	DB().setup(router=dp)
	dp.callback_query.outer_middleware(CallbackFix())