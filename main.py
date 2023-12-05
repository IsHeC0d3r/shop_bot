from asyncio import run
from loader import dp, bot

import middlewares
import handlers
import callbacks
import states


async def on_startup():
    print(f'Bot started succsessfully.')


async def on_shutdown():
    print('Bot stopped succsessfully')


async def init():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await middlewares.init(dp=dp)
    await handlers.init(dp=dp)
    await callbacks.init(dp=dp)
    await states.init(dp=dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(init())
    
# cd $HOME/storage/downloads/projects/shop && python main.py && cd