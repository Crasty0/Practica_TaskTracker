from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Definim schema de baza pentru un task, utilizata ca model comun

class TaskBase(BaseModel):
    title: str = Field(..., example="Proiect")
    description: Optional[str] = Field(None, example="Proiect pentru facultate")
    status: Optional[str] = Field(None, example="to-do")
    deadline: Optional[date] = Field(None, example="2025-09-30")

# Schema utilizata pentru crearea unui task nou
class TaskCreate(TaskBase):
    title: str


from typing import Optional
from pydantic import BaseModel
from datetime import date

# Schema utilizata pentru actualizarea unui task existent

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[date] = None



from datetime import datetime

# Schema utilizata pentru a returna datele unui task catre client
class TaskOut(TaskBase):
    id: int
    owner: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

# Permite utilizarea cu SQLAlchemy ORM
    class Config:
        orm_mode = True
