from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import datetime as dt


# Модели для пользователей
class UserBase(BaseModel):
    id: int
    first_name: str
    surname: str
    email: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    first_name: str
    surname: str
    email: EmailStr  # Используем EmailStr для валидации email
    password: str

    @field_validator("first_name", "surname", "email", "password")
    def no_empty_fields(cls, value):
        if not value or not value.strip():
            raise ValueError(f"Field cannot be empty or blank")
        return value


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


# Модели для товаров
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


# Модели для заказов
class OrderBase(BaseModel):
    user_id: int
    product_id: int
    order_date: dt.datetime
    status: str


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int


class OrderRead(OrderBase):
    id: int

    class Config:
        from_attributes = True
