from app.routes import client_routes
from fastapi import FastAPI
from app.db.database import Base, engine

app = FastAPI()

app.include_router(client_routes.router)
Base.metadata.create_all(bind=engine)