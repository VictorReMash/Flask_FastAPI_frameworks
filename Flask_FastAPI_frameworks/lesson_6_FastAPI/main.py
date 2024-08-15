from fastapi import FastAPI
from app.db import database, engine, metadata
from app import models
from contextlib import asynccontextmanager


# Функция, управляющая жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Подключение к базе данных при старте
    await database.connect()
    yield
    # Отключение от базы данных при завершении
    await database.disconnect()


# Создаем приложение FastAPI и передаем ему функцию lifespan
app = FastAPI(lifespan=lifespan)
# app = FastAPI()
# Создаем все таблицы в базе данных
metadata.create_all(engine)
