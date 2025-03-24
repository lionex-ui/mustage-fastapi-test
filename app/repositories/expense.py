from decimal import ROUND_HALF_UP, Decimal

import httpx
from fastapi import Depends
from sqlalchemy import and_, asc, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ExpenseModel, ExpenseSchema
from app.db.session import get_session
from app.schemas import AddExpenseResponse, DeleteExpenseResponse, EditExpenseResponse, GetExpensesRequest


class ExpensesRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    @staticmethod
    async def _calculate_currency_exchange(uah: Decimal) -> Decimal:
        async with httpx.AsyncClient(http2=True, timeout=10) as client:
            response = await client.get("https://api.privatbank.ua/p24api/pubinfo")
            currencies = response.json()

        sale_rate = None
        for currency in currencies:
            if currency.get("ccy") == "USD":
                sale_rate = Decimal(currency.get("sale"))
                break

        return (uah / sale_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    async def get(self, request_schema: GetExpensesRequest) -> list[ExpenseSchema]:
        query = select(ExpenseModel).filter(ExpenseModel.telegram_id == request_schema.telegram_id)

        if request_schema.from_date is not None and request_schema.to_date is not None:
            query = query.filter(
                and_(ExpenseModel.date >= request_schema.from_date, ExpenseModel.date <= request_schema.to_date)
            )
        elif request_schema.from_date is None and request_schema.to_date is not None:
            query = query.filter(ExpenseModel.date <= request_schema.to_date)
        elif request_schema.from_date is not None and request_schema.to_date is None:
            query = query.filter(ExpenseModel.date >= request_schema.from_date)

        query = query.order_by(asc(ExpenseModel.id))

        result = await self.session.execute(query)
        expenses = result.scalars().all()

        return [ExpenseSchema.model_validate(expense) for expense in expenses]

    async def add(self, expense_scheme: ExpenseSchema) -> AddExpenseResponse:
        usd = await self._calculate_currency_exchange(expense_scheme.uah)

        expense = ExpenseModel(
            telegram_id=expense_scheme.telegram_id,
            title=expense_scheme.title,
            date=expense_scheme.date,
            uah=expense_scheme.uah,
            usd=usd,
        )

        self.session.add(expense)
        await self.session.commit()

        return AddExpenseResponse(result=True)

    async def delete(self, expense_id: int) -> DeleteExpenseResponse:
        await self.session.execute(delete(ExpenseModel).filter(ExpenseModel.id == expense_id))
        await self.session.commit()

        return DeleteExpenseResponse(result=True)

    async def edit(self, expense_scheme: ExpenseSchema) -> EditExpenseResponse:
        result = await self.session.execute(select(ExpenseModel).filter(ExpenseModel.id == expense_scheme.id))
        expense = result.scalar()

        usd = await self._calculate_currency_exchange(expense_scheme.uah)

        expense.title = expense_scheme.title
        expense.uah = expense_scheme.uah
        expense.usd = usd

        await self.session.commit()

        return EditExpenseResponse(result=True)
