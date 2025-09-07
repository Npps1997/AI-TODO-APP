from sqlalchemy.orm import Session
from . import models, schemas

def create_task(db: Session, task_in: schemas.TaskCreate, user_id: int):
    task = models.Task(description=task_in.description, status="pending", user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).order_by(models.Task.id.desc()).all()

def update_task(db: Session, task_id: int, task_in: schemas.TaskUpdate, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if not task:
        return None
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.status is not None:
        task.status = task_in.status
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if not task:
        return None
    db.delete(task)
    db.commit()
    return True
