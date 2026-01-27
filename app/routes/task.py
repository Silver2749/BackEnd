from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate, TaskResponse
from app import get_db

task_router = APIRouter()


@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=None,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return {"msg": "Task created"}


@task_router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()
    return tasks


@task_router.delete("/{task_id}", response_model=dict)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"msg": "Deleted"}
