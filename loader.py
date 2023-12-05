from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database.database import Database
from asyncio import run

from anypay import AnyPayAPI

token = '' # BOT TOKEN
db_url = '' # POSTGRES URL. postgresql+asyncpg:// REQUIRED!!!
logs_chat_id = -100 # LOGS CHAT ID. -100 REQUIRED
admin_tag = '' # SUPPORT TAG (WITH '@')

anypay_api_id = '' # ANYPAY API ID
anypay_api_key = '' # ANYPAY API ID

anypay_api = AnyPayAPI(
    anypay_api_id, anypay_api_key, check=False, project_id=1 # ENABLE check TO STOP BOT IF DATA INVALID
) 

storage = MemoryStorage()

async def init_db():
	return await Database(
		db_url=db_url
	)
db = run(init_db())

dp = Dispatcher(storage=storage)
bot = Bot(
    token=token,
    parse_mode='HTML',
    disable_web_page_preview=True
)