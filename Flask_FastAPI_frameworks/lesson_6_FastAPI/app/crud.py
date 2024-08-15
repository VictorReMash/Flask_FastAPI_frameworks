from sqlalchemy import insert, select, update, delete
from .db import database
from .models import users, products, orders


# CRUD для пользователей
async def create_user(user_data):
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
