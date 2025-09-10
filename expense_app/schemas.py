from pydantic import BaseModel, Field
from typing import Optional


class ExpenseBase(BaseModel):
    title: str 
    amount: float
    
    

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class ExpenseOut(ExpenseBase):
    id: int
    class Config:
        orm_mode = True