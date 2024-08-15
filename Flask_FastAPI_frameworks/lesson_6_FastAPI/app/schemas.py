from pydantic import BaseModel
from typing import Optional
import datetime as dt
import bcrypt


# Модели для пользователей
class UserBase(BaseModel):
    first_name: str
    surname: str
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


# Модели для товаров
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True


# Модели для заказов
class OrderBase(BaseModel):
    user_id: int
    product_id: int
    order_date: dt.datetime
    status: str


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int

    class Config:
        from_attributes = True
