from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from datetime import datetime

from ..base import Base

class User(Base):
	__tablename__ = 'users'
	
	id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
	username = Column(String(32), default='')
	name = Column(String(129), default='') #64 + 64 + 1
	telegram = Column(BigInteger)
	balance = Column(BigInteger, default=0)
	total_payed_amount = Column(BigInteger, default=0)
	admin_lvl = Column(Integer, default=1) #default admin status. 0 - False, 1 - True
	status = Column(Integer, default=0)
	time = Column(DateTime, default=datetime.utcnow)