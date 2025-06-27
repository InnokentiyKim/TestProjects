import uuid

from config import PG_DSN
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, DateTime, Integer, func, UUID, ForeignKey, CheckConstraint
import datetime
from custom_types import Role


engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class User(Base):
    __tablename__ = "user"
    __tableargs__ = (
        CheckConstraint("role in ('user', 'admin')")
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    tokens: Mapped[list["Token"]] = relationship("Token", lazy="joined", back_populates="user")
    todos: Mapped[list["ToDo"]] = relationship("ToDo", lazy="joined", back_populates="user")
    role: Mapped[Role] = mapped_column(String, default="user")


class Token(Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, server_default=func.gen_random_uuid())
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(User, lazy="joined", back_populates="tokens")

    @property
    def to_dict(self):
        return {"token": self.token}


class ToDo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    important: Mapped[bool] = mapped_column(Boolean, default=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(User, lazy="joined", back_populates="todos")

    @property
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "important": self.important,
            "done": self.done,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None
        }


ORM_OBJ = ToDo | User | Token
ORM_CLS = type[ToDo] | type[User] | type[Token]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()