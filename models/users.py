import enum
from datetime import datetime

from sqlalchemy import String, Enum, BigInteger, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Model


class Channel(Model):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    chat_id: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(String(255), unique=True)


class User(Model):
    class Type(enum.Enum):
        ADMIN = 'admin'
        USER = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    type: Mapped[Type] = mapped_column(Enum(Type), server_default=Type.USER.name)
    username: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    @classmethod
    def get_or_create(cls, **kwargs) -> tuple['User', bool]:
        user = cls.get(kwargs.get('id'))
        if user is None:
            user = cls.create(**kwargs)
            return user, True
        return user, False

    @property
    def is_admin(self) -> bool:
        return self.type == self.Type.ADMIN
