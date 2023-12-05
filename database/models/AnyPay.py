from sqlalchemy import Column, Integer, BigInteger, String

from ..base import Base

class AnyPay(Base):
	__tablename__ = 'anypay'
	
	id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
	telegram = Column(BigInteger)
	transaction_id = Column(BigInteger, default=None)
	amount = Column(BigInteger, default=None)
	status = Column(Integer, default=0)