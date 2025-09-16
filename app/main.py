from fastapi import FastAPI, Depends, HTTPException, Query, Response, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .db import engine, Base, get_db
from .utils import get_current_user
from fastapi.responses import StreamingResponse
import csv
import io


# creează tabelele dacă nu există
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Task Manager API")


@app.post("/tasks", response_model=schemas.TaskOut)
async def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db), owner: Optional[str] = Depends(get_current_user)):
    task = crud.create_task(db, task_in, owner=owner)
    return task


@app.get("/tasks", response_model=List[schemas.TaskOut])
async def list_tasks(status: Optional[str] = Query(None), due_before: Optional[str] = Query(None), db: Session = Depends(get_db), owner: Optional[str] = Depends(get_current_user)):
    # due_before expected format YYYY-MM-DD
    from datetime import datetime
    due = None
    if due_before:
        try:
            due = datetime.strptime(due_before, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="deadline must be YYYY-MM-DD")
    tasks = crud.list_tasks(db, owner=owner, status=status, due_before=due)
    return tasks

from datetime import date
from app import models, schemas

app = FastAPI()

@app.get("/tasks", response_model=List[schemas.TaskOut])
def read_tasks(
    status: Optional[str] = None,       # filtru după status
    due_before: Optional[date] = None,  # filtru după deadline
    db: Session = Depends(get_db),
    user: str = Header(..., alias = "X-User")
):
    query = db.query(models.Task).filter(models.Task.owner == user)

    if status:
        query = query.filter(models.Task.status == status)
    if due_before:
        query = query.filter(models.Task.deadline <= due_before)

    return query.all()



@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
async def update_task(task_id: int, changes: schemas.TaskUpdate, db: Session = Depends(get_db), owner: Optional[str] = Depends(get_current_user)):
    task = crud.get_task(db, task_id)
    if not task or (owner and task.owner != owner):
        raise HTTPException(status_code=404, detail="Task not found")
    updated = crud.update_task(db, task, changes)
    return updated


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db), owner: Optional[str] = Depends(get_current_user)):
    task = crud.get_task(db, task_id)
    if not task or (owner and task.owner != owner):
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
    return {"ok": True}


@app.get("/tasks/export")
async def export_tasks(
    format: Optional[str] = Query("csv"),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    owner: Optional[str] = Depends(get_current_user)
):
    tasks = crud.list_tasks(db, owner=owner, status=status)

    if format == "json":
        return [t.__dict__ for t in tasks]

    # CSV
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(["id", "title", "description", "status", "deadline", "owner", "created_at"])

    for t in tasks:
        writer.writerow([
            t.id,
            t.title,
            t.description,
            t.status,
            t.deadline.isoformat() if t.deadline else "",
            t.owner,
            t.created_at.isoformat() if t.created_at else ""
        ])

    stream.seek(0)
    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tasks.csv"}
    )
