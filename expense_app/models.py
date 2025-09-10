from sqlalchemy import Column, Integer, String, Float
from database import Base


    
class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer,primary_key=True)
    title = Column(String)
    amount = Column(Float)
    description = Column(String)
    
    
    
    