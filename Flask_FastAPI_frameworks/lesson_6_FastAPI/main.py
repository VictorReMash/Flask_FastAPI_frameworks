from fastapi import FastAPI
from app.db import database, engine, metadata
from app import models
from contextlib import asynccontextmanager


# Функция, управляющая жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):

    await database.connect()
    yield

    await database.disconnect()


# Создаем приложение FastAPI и передаем ему функцию lifespan
app = FastAPI(lifespan=lifespan)

# Создаем все таблицы в базе данных
metadata.create_all(engine)
