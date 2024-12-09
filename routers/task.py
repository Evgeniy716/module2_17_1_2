from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import Task
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    if task is not None:
        return task
    raise HTTPException(status_code=404, detail="Task was not found")


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)],
                      task_create_model: CreateTask = None, user_id: int = None):
    try:
        db.execute(insert(Task).values(title=task_create_model.title,
                                       content=task_create_model.content,
                                       priority=task_create_model.priority,
                                       completed=task_create_model.completed,
                                       user_id=user_id,
                                       slug=slugify(task_create_model.task)
                                       ))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED,
                'transaction': 'Successful!'}
    except:
        raise HTTPException(status_code=404, detail="User was not found")


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int, task_update_model: UpdateTask):
    task = db.scalars(select(Task).where(Task.id == task_id))
    for u in task:
        if u is not None:
            db.execute(update(Task).where(Task.id == task_id).values(
                title=task_update_model.title,
                content=task_update_model.content,
                priority=task_update_model.priority,
                completed=task_update_model.completed,
                user_id=task_update_model.user_id,
                slug=slugify(task_update_model.task)
            ))
            db.commit()
            return {'status_code': status.HTTP_200_OK,
                    'transaction': 'User update is successful!'}
            raise HTTPException(status_code=404, detail="User was not found")


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    for u in task:
        if task is not None:
            db.execute(delete(Task).where(Task.id == task_id))
            db.commit()
            return {'status_code': status.HTTP_200_OK,
                    'transaction': 'User update is successful!'}
        raise HTTPException(status_code=404, detail="User was not found")
