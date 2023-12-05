from sqlalchemy import Column, Integer, BigInteger, String

from ..base import Base

class Cart(Base):
	__tablename__ = 'cart'
	
	id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
	telegram = Column(BigInteger)
	category_id = Column(BigInteger, default=0)
	product_id = Column(BigInteger, default=0)
	name = Column(String(50), default=None)
	price = Column(BigInteger, default=0)
	count = Column(BigInteger, default=1)