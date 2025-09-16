from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class TaskBase(BaseModel):
    title: str = Field(..., example="Cumparaturi")
    description: Optional[str] = Field(None, example="Laptele, paine, oua")
    status: Optional[str] = Field(None, example="to-do")
    deadline: Optional[date] = Field(None, example="2025-09-30")


class TaskCreate(TaskBase):
    title: str


from typing import Optional
from pydantic import BaseModel
from datetime import date

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[date] = None



from datetime import datetime

class TaskOut(TaskBase):
    id: int
    owner: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
