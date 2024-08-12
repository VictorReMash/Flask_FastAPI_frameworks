from typing import Optional
from pydantic import BaseModel


# Модель для задачи, которую пользователь отправляет (без id)
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False


# Модель для задачи, возвращаемая сервером (с id)
class Task(TaskCreate):
    id: int
