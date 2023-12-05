from sqlalchemy import Column, Integer, BigInteger, String

from ..base import Base

class Purchase(Base):
	__tablename__ = 'purchases'
	
	id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
	telegram = Column(BigInteger)
	product_name = Column(String(50), default=None)
	product_price = Column(Integer, default=None)
	product_discount = Column(Integer, default=None)
	product_count = Column(Integer, default=1)