from aiogram import Dispatcher

import callbacks.admin as admin
import callbacks.user as user

async def init(dp: Dispatcher) -> None:
    await admin.init(dp)
    await user.init(dp)