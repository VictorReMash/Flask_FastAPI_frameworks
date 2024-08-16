from sqlalchemy import insert, select, update, delete
from .db import database
from .models import users, products, orders
from fastapi import HTTPException
import bcrypt


# CRUD для пользователей
async def create_user(user_data):
    # Проверяем, существует ли уже пользователь с таким email
    query = select(users).where(users.c.email == user_data["email"])
    existing_user = await database.fetch_one(query)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    # Хэшируем пароль перед сохранением
    hashed_password = bcrypt.hashpw(
        user_data["password"].encode("utf-8"), bcrypt.gensalt()
    )
    user_data["password"] = hashed_password.decode(
        "utf-8"
    )  # Преобразуем обратно в строку для хранения

    # Если email уникален, создаем нового пользователя
    query = insert(users).values(**user_data)
    return await database.execute(query)


# CRUD для пользователей
async def get_all_users():
    query = select(users)
    return await database.fetch_all(query)


async def get_user(user_id: int):
    query = select(users).where(users.c.id == user_id)
    return await database.fetch_one(query)


async def update_user(user_id: int, user_data):
    query = update(users).where(users.c.id == user_id).values(**user_data)
    await database.execute(query)
    return await get_user(user_id)


async def delete_user(user_id: int):
    query = delete(users).where(users.c.id == user_id)
    await database.execute(query)


# CRUD для товаров
async def get_product(product_id: int):
    query = select(products).where(products.c.id == product_id)
    return await database.fetch_one(query)


async def create_product(product_data):
    query = insert(products).values(**product_data)
    return await database.execute(query)


async def update_product(product_id: int, product_data):
    query = update(products).where(products.c.id == product_id).values(**product_data)
    await database.execute(query)
    return await get_product(product_id)


async def delete_product(product_id: int):
    query = delete(products).where(products.c.id == product_id)
    await database.execute(query)


# CRUD для заказов
async def get_order(order_id: int):
    query = select(orders).where(orders.c.id == order_id)
    return await database.fetch_one(query)


async def create_order(order_data):
    # Проверка существования пользователя и продукта
    user_exists = await database.fetch_one(
        select(users).where(users.c.id == order_data["user_id"])
    )
    product_exists = await database.fetch_one(
        select(products).where(products.c.id == order_data["product_id"])
    )

    if not user_exists or not product_exists:
        raise HTTPException(status_code=400, detail="Invalid user_id or product_id")

    # Создание заказа
    query = insert(orders).values(**order_data)
    order_id = await database.execute(query)
    return order_id


async def update_order(order_id: int, order_data):
    query = update(orders).where(products.c.id == order_id).values(**order_data)
    await database.execute(query)
    return await get_order(order_id)


async def delete_order(order_id: int):
    query = delete(orders).where(orders.c.id == order_id)
    await database.execute(query)
