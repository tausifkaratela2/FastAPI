from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

expenses = {}
next_id = 1

class Expense(BaseModel):
    description: str
    category: str
    amount: float

def check_expense(exp: Expense):
    if not exp.description.strip():
        raise HTTPException(status_code=400, detail="Description cannot be empty")
    if exp.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

@app.post("/expenses")
def add_expense(exp: Expense):
    global next_id
    check_expense(exp)

    new_expense = {
        "id": next_id,
        "description": exp.description,
        "category": exp.category,
        "amount": exp.amount
    }
    expenses[next_id] = new_expense
    next_id += 1
    return {"message": "Expense added successfully", "expense": new_expense}

@app.get("/expenses")
def get_expenses():
    return list(expenses.values())

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
    return {"message": "Expense deleted successfully"}

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, exp: Expense):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    check_expense(exp)
    
    updated_expense = {
        "id": expense_id,
        "description": exp.description,
        "category": exp.category,
        "amount": exp.amount
    }
    expenses[expense_id] = updated_expense
    return {"message": "Expense updated successfully", "expense": updated_expense}