from fastapi import FastAPI, HTTPException, status, Path, Query
from fastapi.responses import JSONResponse
from typing import Dict


app = FastAPI()

expenses: Dict[int, Dict] = {}
current_id = 0

@app.get('/')
def get_all_expenses():
    content = expenses
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@app.post('/create')
def create_expense(item_name:str= Query(...), amount:float=Query(gt=0), description:str=Query(default='')):
    global current_id
    current_id += 1
    
    item = {
        'id': current_id,
        'item_name':item_name,
        'description': description,
        'amount': amount,
    }
    expenses[current_id] = item
    return JSONResponse(content=f'add {item_name} sucssesfully.', status_code=status.HTTP_201_CREATED) 
    


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int = Path(..., ge=1)):
    if expense_id not in expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expenses[expense_id]
    
      
@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int = Path(..., ge=1),
    item_name: str = Query(...),
    amount: float = Query(..., gt=0),
    description: str = Query("")):
    
    if expense_id not in expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    expenses[expense_id].update({
        "item_name": item_name,
        "amount": amount,
        "description": description
    })
    


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int = Path(..., ge=1)):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
    return {"message": f"Expense {expense_id} deleted successfully"} 
