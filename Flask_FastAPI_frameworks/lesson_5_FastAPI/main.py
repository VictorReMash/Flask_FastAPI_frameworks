import logging
from fastapi import FastAPI, HTTPException
from typing import List
from models import Task, TaskCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Хранилище для задач (имитация базы данных)
tasks = {}
task_id_counter = 1


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    logger.info("Отработал GET запрос по всем существующим задачам.")
    return list(tasks.values())


@app.get("/tasks/{id}", response_model=Task)
def get_task(id: int):
    if id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info("Отработал GET запрос отбора задачи по id.")
    return tasks[id]


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global task_id_counter
    # Присваиваем идентификатор задаче
    task_with_id = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
    )
    tasks[task_id_counter] = task_with_id
    task_id_counter += 1
    logger.info("Отработал POST запрос по созданию задачи.")
    return tasks[task_with_id.id]


@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, updated_task: TaskCreate):
    if id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    # Обновляем задачу, сохраняя её идентификатор
    updated_task_with_id = Task(
        id=id,
        title=updated_task.title,
        description=updated_task.description,
        is_completed=updated_task.is_completed,
    )
    logger.info("Отработал PUT запрос по изменению задачи.")
    tasks[id] = updated_task_with_id
    return tasks[id]


@app.delete("/tasks/{id}", response_model=dict)
def delete_task(id: int):
    if id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[id]
    logger.info("Отработал DELETE запрос по удалению задачи.")
    return {"message": "Task deleted successfully"}
