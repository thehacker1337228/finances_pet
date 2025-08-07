import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import time

engine = create_async_engine("sqlite+aiosqlite:///data/user_data.db", pool_pre_ping=True)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    def __init__(self, id, name, description, user_id, created_at):
        self.id = id
        self.name = name
        self.description = description
        self.user_id = user_id
        self.created_at = created_at


class Wastes(Base):
    __tablename__ = 'wastes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    amount: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    def __init__(self, id, category_id, amount, user_id, created_at):
        self.id = id
        self.category_id = category_id
        self.amount = amount
        self.user_id = user_id
        self.created_at = created_at

class Limits(Base):
    __tablename__ = 'limits'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    amount: Mapped[int] = mapped_column(nullable=False)
    begin_date: Mapped[str] = mapped_column(nullable=False)
    end_date: Mapped[str] = mapped_column(nullable=False)
    one_time: Mapped[int] = mapped_column(nullable=False)

    def __init__(self, id, category_id, amount, user_id, end_date, one_time):
        self.id = id
        self.category_id = category_id
        self.amount = amount
        self.user_id = user_id
        self.created_at = created_at
        self.end_date = end_date
        self.one_time = one_time




async def init_main(): #функция создающая все эти таблицы если их не существует
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("создание таблиц если не существуют")

