from aiogram import Dispatcher, F

import handlers.admin as admin
import handlers.user as user

async def init(dp: Dispatcher) -> None:
	await admin.init(dp=dp)
	await user.init(dp=dp)