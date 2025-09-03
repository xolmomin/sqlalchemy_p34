from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Model


class Category(Model):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')

    def __str__(self):
        return f"{self.id} - {self.name}"


class Product(Model):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', back_populates='products')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __str__(self):
        return f"{self.id} - {self.name}"
