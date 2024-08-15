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


async def get_user(user_id: int):
    query = select(users).where(users.c.id == user_id)
    return await database.fetch_one(query)


async def get_all_users():
    query = select(users)
    return await database.fetch_all(query)


async def update_user(user_id: int, user_data):
    query = update(users).where(users.c.id == user_id).values(**user_data)
    await database.execute(query)
    return await get_user(user_id)


async def delete_user(user_id: int):
    query = delete(users).where(users.c.id == user_id)
    await database.execute(query)


# Аналогичные CRUD функции можно создать для товаров и заказов
