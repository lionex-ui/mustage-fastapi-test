from fastapi import APIRouter

from app.api.v1 import expense

router = APIRouter()
router.include_router(expense.router)
