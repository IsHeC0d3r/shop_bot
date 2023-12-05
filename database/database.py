from misc.AioObject import AioObject
from .base import Base

from .models.User import User
from .models.Purchase import Purchase
from .models.Category import Category
from .models.Product import Product
from .models.Cart import Cart
from .models.AnyPay import AnyPay

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from sqlalchemy.engine import Result
from typing import Any
from sqlalchemy.sql.expression import Executable

class Database(AioObject):
	async def __init__(self, db_url) -> object:
		engine = create_async_engine(
			db_url,
			future = True,
			poolclass=NullPool
		)
		
		async with engine.begin() as conn:
			await conn.run_sync(Base.metadata.create_all)
    
		self.session = async_sessionmaker(engine, expire_on_commit=False)