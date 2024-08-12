import logging
from fastapi import FastAPI

from typing import Optional
from pydantic import BaseModel

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

app = FastAPI()

#
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None


@app.get("/")
async def read_root():
    # logger.info("Отработал GET запрос.")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    # logger.info("Отработал POST запрос.")
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/users/{user_id}/orders/{order_id}")
async def read_data(user_id: int, order_id: int):
    # logger.info(f"Отработал PUT запрос для item id = {item_id}.")
    return {"user_id": user_id, "order_id": order_id}


#
#
# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     logger.info(f"Отработал DELETE запрос для item id ={item_id}.")
#     return {"item_id": item_id}
