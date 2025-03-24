from fastapi import APIRouter, Depends

from app.db.models import ExpenseSchema
from app.repositories import ExpensesRepository
from app.schemas import AddExpenseResponse, DeleteExpenseResponse, EditExpenseResponse, GetExpensesRequest

router = APIRouter(prefix="/expenses", tags=["Управління статтями витрат"])


@router.get("", response_model=list[ExpenseSchema])
async def get_expenses(
    request_schema: GetExpensesRequest = Depends(GetExpensesRequest), expenses_repo: ExpensesRepository = Depends()
):
    return await expenses_repo.get(request_schema)


@router.post("", response_model=AddExpenseResponse)
async def add_expense(expense_schema: ExpenseSchema, expenses_repo: ExpensesRepository = Depends()):
    return await expenses_repo.add(expense_schema)


@router.put("", response_model=EditExpenseResponse)
async def edit_expense(expense_schema: ExpenseSchema, expenses_repo: ExpensesRepository = Depends()):
    return await expenses_repo.edit(expense_schema)


@router.delete("/{expense_id}", response_model=DeleteExpenseResponse)
async def delete_expense(expense_id: int, expense_repo: ExpensesRepository = Depends()):
    return await expense_repo.delete(expense_id)
