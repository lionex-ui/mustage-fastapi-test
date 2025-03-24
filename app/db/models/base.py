from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase


def alias_generator(s: str) -> str:
    return "".join([word.capitalize() if i > 0 else word for i, word in enumerate(s.split("_"))])


class Model(DeclarativeBase):
    pass


class Schema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=alias_generator, from_attributes=True)
