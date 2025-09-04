from fastapi import FastAPI, HTTPException, status, Path, Body
from typing import Dict, List
from schama import Expense, ExpenseCreate, ExpenseUpdate

app = FastAPI()

expenses: Dict[int, Expense] = {}
current_id = 0

@app.get('/', tags=["Root"])
def root():
    return {"message": "this is main page"}

@app.get('/expenses', response_model=List[Expense], tags=["Expenses"])
def get_all_expenses():
    return list(expenses.values())

@app.post("/create", response_model=Expense, status_code=status.HTTP_201_CREATED, tags=["Expenses"])
def create_expense(expense: ExpenseCreate):
    global current_id
    current_id += 1
    new_expense = Expense(id=current_id, **expense.model_dump())
    expenses[current_id] = new_expense
    return new_expense

@app.get("/expenses/{expense_id}", response_model=Expense, tags=["Expenses"])
def get_expense(expense_id: int = Path(..., ge=1)):
    if expense_id not in expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expenses[expense_id]

@app.put("/expenses/{expense_id}", response_model=Expense, tags=["Expenses"])
def update_expense(
    expense_id: int = Path(..., ge=1),
    updated_expense: ExpenseUpdate = Body(...)
):
    if expense_id not in expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    updated = Expense(id=expense_id, **updated_expense.model_dump())
    expenses[expense_id] = updated
    return updated

@app.delete("/expenses/{expense_id}", tags=["Expenses"])
def delete_expense(expense_id: int = Path(..., ge=1)):
    if expense_id not in expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    del expenses[expense_id]
    return {"message": f"Expense {expense_id} deleted successfully"}
