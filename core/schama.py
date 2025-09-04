from pydantic import BaseModel, Field
from typing import Optional


class ExpenseBase(BaseModel):
    item_name: str = Field(..., min_length=1, example="Groceries")
    amount: float = Field(..., gt=0, example=150.0)
    description: Optional[str] = Field("", max_length=255, example="Bought fruits and vegetables")

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int