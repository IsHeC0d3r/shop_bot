from sqlalchemy import Column, Integer, BigInteger, String

from ..base import Base

class Product(Base):
	__tablename__ = 'products'
	
	id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
	category = Column(BigInteger, default=0)
	photo = Column(String(length=250), default=None)
	name = Column(String(50), default=None)
	description = Column(String(250), default=None)
	price = Column(BigInteger, default=None)
	discount = Column(Integer, default=None)
	count = Column(BigInteger, default=1)