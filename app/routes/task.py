from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Task, User
from app.schemas import TaskCreate, TaskResponse
from app import get_db
from app.routes.auth import get_current_user

task_router = APIRouter()


@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
   
    task = Task(         #new task
        title=task_data.title,
        description=task_data.description,
        user_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return {"msg": "Task created", "task_id": task.id}


@task_router.get("/", response_model=list[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
   
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks


@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
   
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    
    if task.user_id != current_user.id:        #if task belongs to the user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this task"
        )
    
    return task


@task_router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    
    task = db.query(Task).filter(Task.id == task_id).first()    #update task
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this task"
        )
    
    task.title = task_data.title
    task.description = task_data.description
    db.commit()
    db.refresh(task)
    
    return task


@task_router.delete("/{task_id}", response_model=dict)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
   
    task = db.query(Task).filter(Task.id == task_id).first()     #delete task
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
  
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this task"
        )

    db.delete(task)
    db.commit()

    return {"msg": "Task deleted"}

