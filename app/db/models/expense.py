from datetime import datetime
from decimal import Decimal

from pydantic import Field
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Model, Schema


class ExpenseModel(Model):
    __tablename__ = "expense"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    title: Mapped[str] = mapped_column(String(64))
    date: Mapped[datetime]
    uah: Mapped[Decimal] = mapped_column(Numeric(precision=9, scale=2))
    usd: Mapped[Decimal] = mapped_column(Numeric(precision=9, scale=2))


class ExpenseSchema(Schema):
    id: int | None = Field(default=None)
    telegram_id: int = Field(alias="telegramId")
    title: str = Field(max_length=64)
    date: datetime
    uah: Decimal = Field(max_digits=9, decimal_places=2)
    usd: Decimal | None = Field(max_digits=9, decimal_places=2, default=None)
