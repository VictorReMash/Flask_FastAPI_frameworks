from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app import crud
from app.db import database, engine, metadata
import app.schemas as sch
import uvicorn
from typing import List
import bcrypt


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

metadata.create_all(engine)


@app.post("/users", response_model=sch.UserBase)
async def create_user(user: sch.UserCreate):
    user_id = await crud.create_user(user.model_dump())
    return {**user.model_dump(), "id": user_id}


@app.get("/user/{id}", response_model=sch.UserBase)
async def read_user(user_id: int):
    user = await crud.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users", response_model=List[sch.UserBase])
async def read_users():
    users = await crud.get_all_users()
    return users


@app.put("/users/{user_id}", response_model=sch.UserBase)
async def update_user(user_id: int, user: sch.UserUpdate):
    # Преобразование Pydantic модели в словарь, удаление ключей со значением None
    user_data = user.dict(exclude_unset=True)

    # Проверка существования пользователя
    existing_user = await crud.get_user(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Хэширование нового пароля, если он был предоставлен
    if "password" in user_data:
        user_data["password"] = bcrypt.hashpw(
            user_data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    updated_user = await crud.update_user(user_id, user_data)
    return updated_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # Проверка существования пользователя
    existing_user = await crud.get_user(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    await crud.delete_user(user_id)
    return {"detail": "User deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
