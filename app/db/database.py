from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Usa DATABASE_URL, que vem do docker-compose.yml
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/lu_estilo")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
