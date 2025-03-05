from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __allow_unmapped__ = True
    __table_args__ = {"schema": "public"}
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

        

# This is a base class for SQLAlchemy models. When you define your models, you should inherit from this base class. For example:

# ```python
# from sqlalchemy import Column, Integer, String
# from .base import Base