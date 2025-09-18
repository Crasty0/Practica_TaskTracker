from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Date
from sqlalchemy.sql import func
from .db import Base
import enum

# Enum pentru statusurile posibile ale unui task
class StatusEnum(str, enum.Enum):
    todo = "to-do"
    in_progress = "in-progress"
    done = "done"

# Modelul pentru tabela "tasks" din baza de date
class Task(Base):
    __tablename__ = "tasks"


    id = Column(Integer, primary_key=True, index=True)                          #Primary key
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)                                   #optional
    status = Column(String(32), default=StatusEnum.todo.value)                  #implicit to-do
    deadline = Column(Date, nullable=True)                                      #optional
    owner = Column(String(100), nullable=True)                                  #optional
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())