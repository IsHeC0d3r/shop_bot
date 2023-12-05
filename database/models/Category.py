from sqlalchemy import Column, Integer, BigInteger, String

from ..base import Base

class Category(Base):
	__tablename__ = 'categories'
	
	id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
	name = Column(String(50), default=None)