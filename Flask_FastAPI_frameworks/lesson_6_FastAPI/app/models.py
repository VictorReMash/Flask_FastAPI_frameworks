import datetime as dt
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from .db import metadata

# Определение таблицы пользователи
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(32)),
    Column("surname", String(32)),
    Column("email", String(128)),
    Column("password", String(16)),
)

# Определение таблицы товары
products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(128)),
    Column("description", String(256)),
    Column("price", Integer),
)

# Определение таблицы заказы покупателей
orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("order_date", DateTime, default=lambda: dt.datetime.now(dt.timezone.utc)),
    Column("status", String(32)),
)
database_table_models
