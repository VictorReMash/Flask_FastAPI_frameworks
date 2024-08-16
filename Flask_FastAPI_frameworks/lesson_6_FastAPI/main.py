from fastapi import FastAPI, HTTPException, Path
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


# *** БЛОК чтения записей БД по id
@app.get("/user/{id}", response_model=sch.UserBase)
async def read_user(user_id: int):
    user = await crud.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/product/{id}", response_model=sch.ProductRead)
async def read_product(product_id: int):
    product = await crud.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/orders/{order_id}", response_model=sch.OrderBase)
async def read_order(order_id: int):
    order = await crud.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# *** получаем список всех пользователей
@app.get("/users", response_model=List[sch.UserBase])
async def read_users():
    users = await crud.get_all_users()
    return users


# *** БЛОК создания записей в БД
@app.post("/user", response_model=sch.UserBase)
async def create_user(user: sch.UserCreate):
    user_id = await crud.create_user(user.model_dump())
    return {**user.model_dump(), "id": user_id}


@app.post("/product", response_model=sch.ProductBase)
async def create_product(product: sch.ProductBase):
    product_id = await crud.create_product(product.model_dump())
    return {**product.model_dump(), "id": product_id}


@app.post("/order", response_model=sch.Order)
async def create_product(order: sch.OrderCreate):
    order_id = await crud.create_order(order.model_dump())
    return {**order.model_dump(), "id": order_id}


# *** БЛОК обновления записей в БД
@app.put("/users/{user_id}", response_model=sch.UserBase)
async def update_user(user_id: int, user: sch.UserUpdate):
    # Преобразование Pydantic модели в словарь, удаление ключей со значением None
    user_data = user.model_dump(exclude_unset=True)

    # Проверка существования пользователя
    existing_user = await crud.get_user(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Хэш нового пароля, если он был предоставлен
    if "password" in user_data:
        user_data["password"] = bcrypt.hashpw(
            user_data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    updated_user = await crud.update_user(user_id, user_data)
    return updated_user


@app.put("/products/{product_id}", response_model=sch.ProductBase)
async def update_product(product_id: int, product: sch.ProductUpdate):
    existing_product = await crud.get_product(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Обновляем продукт в базе данных
    updated_product = await crud.update_product(product_id, product.model_dump())
    return updated_product


@app.put("/orders/{order_id}", response_model=sch.OrderBase)
async def update_order(order_id: int, order: sch.OrderCreate):
    existing_order = await crud.get_order(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await crud.update_order(order_id, order.model_dump())
    return updated_order


# *** БЛОК удаления записей в таблице USERS
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # Проверка существования пользователя
    existing_user = await crud.get_user(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    await crud.delete_user(user_id)
    return {"detail": "User deleted successfully"}


@app.delete("/products/{product_id}")
async def delete_order(product_id: int):
    existing_product = await crud.get_product(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    await crud.delete_product(product_id)
    return {"detail": "Product deleted successfully"}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    existing_order = await crud.get_order(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    await crud.delete_order(order_id)
    return {"detail": "Order deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
