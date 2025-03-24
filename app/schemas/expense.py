from datetime import datetime

from pydantic import BaseModel, Field


class GetExpensesRequest(BaseModel):
    telegram_id: int = Field(alias="telegramId")
    from_date: datetime | None = Field(alias="fromDate", default=None)
    to_date: datetime | None = Field(alias="toDate", default=None)


class AddExpenseResponse(BaseModel):
    result: bool


class DeleteExpenseResponse(BaseModel):
    result: bool


class EditExpenseResponse(BaseModel):
    result: bool
