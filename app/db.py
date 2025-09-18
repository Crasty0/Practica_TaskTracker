from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Definim calea bazei de date SQLite, utilizand o variabila de mediu sau o valoare implicita
DB_PATH = os.getenv("TASKS_DB", "./tasks.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Cream engine-ul SQLAlchemy pentru baza de date SQLite
engine = create_engine(
SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# helper dependency for FastAPI
# Functie helper pentru a obtine o sesiune a bazei de date in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()