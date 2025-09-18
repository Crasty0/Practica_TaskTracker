from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from datetime import date

# Creeaza un task nou in baza de date
def create_task(db: Session, task_in: schemas.TaskCreate, owner: Optional[str] = None):
    db_task = models.Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status or models.StatusEnum.todo.value,
        deadline=task_in.deadline,
        owner=owner,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Returneaza un task dupa ID
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# Listeaza task-urile, cu filtre optionale
def list_tasks(db: Session, owner: Optional[str] = None, status: Optional[str] = None, due_before: Optional[date] = None):
    q = db.query(models.Task)
    if owner:
        q = q.filter(models.Task.owner == owner)
    if status:
        q = q.filter(models.Task.status == status)
    if due_before:
        q = q.filter(models.Task.deadline != None).filter(models.Task.deadline <= due_before)
    return q.order_by(models.Task.id).all()

# Actualizeaza un task existent
def update_task(db: Session, task: models.Task, changes: schemas.TaskUpdate):
    for field, value in changes.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# Sterge un task din baza de date
def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()
    return True