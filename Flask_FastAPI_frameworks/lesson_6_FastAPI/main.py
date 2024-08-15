from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app import crud
from app.db import database, engine, metadata
import app.schemas as sch
import uvicorn


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


@app.post("/users", response_model=sch.UserBase)
async def create_user(user: sch.UserCreate):
    user_id = await crud.create_user(user.model_dump())
    return {**user.model_dump(), "id": user_id}


@app.get("/users/{id}", response_model=sch.UserBase)
async def read_user(user_id: int):
    user = await crud.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
