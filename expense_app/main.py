from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, Base, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post('/expenses/', response_model=schemas.ExpenseOut)
def create_expense(expense: schemas.ExpenseCreate, db: Session= Depends(get_db)):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get('/expenses/', response_model=list[schemas.ExpenseOut])
def read_expenses(skip: int = 0, limit:int = 10, db:Session=Depends(get_db)):
    return db.query(models.Expense).offset(skip).limit(limit).all()

@app.get('/expenses/{expense_id}', response_model=schemas.ExpenseOut)
def read_expense(expense_id: int, db: Session= Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Not Found")
    return expense

@app.put('/expenses/{expense_id}',response_model=schemas.ExpenseOut)
def update_expense(expense_id : int, expense_update: schemas.ExpenseUpdate, db:Session= Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Not Found")
    
    update_data = expense_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(expense, key, value)
    
    db.commit()
    db.refresh(expense)
    return expense

@app.delete('/expenses/{expense_id}')
def delete_expense(expense_id: int, db:Session= Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Not Found")
    db.delete(expense)
    db.commit()
    return {"message": "deleted succsessfully"}