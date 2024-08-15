from typing import Optional
from pydantic import BaseModel
from pydantic import field_validator


# Модель для задачи, которую пользователь отправляет (без id)
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

    @field_validator("title")
    def non_empty_header_value(cls, value):
        if not value.strip():
            raise ValueError("Заголовок задачи не может быть пустым!")
        return value


# Модель для задачи, возвращаемая сервером (с id)
class Task(TaskCreate):
    id: int
