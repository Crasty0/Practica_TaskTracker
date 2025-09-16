from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Date
from sqlalchemy.sql import func
from .db import Base
import enum


class StatusEnum(str, enum.Enum):
    todo = "to-do"
    in_progress = "in-progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"


    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(32), default=StatusEnum.todo.value)
    deadline = Column(Date, nullable=True)
    owner = Column(String(100), nullable=True) # optional simple "user"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())