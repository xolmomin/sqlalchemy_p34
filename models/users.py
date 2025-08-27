import bcrypt
from sqlalchemy import Integer, String, select as sqlalchemy_select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Model, db


class User(Model):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='created_by')

    def __str__(self):
        return f"{self.id} - {self.username}"

    @classmethod
    def get_by_username(cls, _username: str):
        query = sqlalchemy_select(cls).where(cls.username == _username)
        results = db.execute(query)
        return results.scalar()

    @staticmethod
    def get_hash_password(_password: str):
        hashed_password = bcrypt.hashpw(_password.encode(), bcrypt.gensalt())
        return hashed_password.decode()

    @staticmethod
    def check_hash_password(_password: str, hashed_password: str):
        return bcrypt.checkpw(_password.encode(), hashed_password.encode())
