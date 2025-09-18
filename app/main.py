from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
import csv, io

from . import models, schemas, crud
from .db import engine, Base, get_db
from .utils import get_current_user

# Creeaza tabelele daca nu exista
Base.metadata.create_all(bind=engine)

# Initializeaza aplicatia FastAPI
app = FastAPI(title="Task Manager API")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTES ---------------- #

# Ruta pentru crearea unui task nou
@app.post("/tasks", response_model=schemas.TaskOut)
async def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    owner: Optional[str] = Depends(get_current_user)  # X-User optional la OPTIONS
):
    return crud.create_task(db, task_in, owner=owner)

# Ruta pentru listarea task-urilor existente
@app.get("/tasks", response_model=List[schemas.TaskOut])
async def list_tasks(
    status: Optional[str] = Query(None),
    due_before: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    owner: Optional[str] = Depends(get_current_user)
):
    due = None
    if due_before:
        try:
            # Convertim string-ul deadline in format de data
            due = datetime.strptime(due_before, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="deadline must be YYYY-MM-DD")
    return crud.list_tasks(db, owner=owner, status=status, due_before=due)

# Ruta pentru actualizarea unui task existent
@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
async def update_task(
    task_id: int,                       # ID-ul task-ului de actualizat
    changes: schemas.TaskUpdate,        # Schimbarile de aplicat
    db: Session = Depends(get_db),
    owner: Optional[str] = Depends(get_current_user)
):
    task = crud.get_task(db, task_id)
    if not task or (owner and task.owner != owner):
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, task, changes)

# Ruta pentru stergerea unui task
@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    owner: Optional[str] = Depends(get_current_user)
):
    task = crud.get_task(db, task_id)
    if not task or (owner and task.owner != owner):
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
    return {"ok": True}

# Ruta pentru exportarea task-urilor in format CSV sau JSON
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
