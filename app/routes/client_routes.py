from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.client_entity import Client
from app.schemas.client_schemas import ClientCreate, ClientOut
from typing import List


router = APIRouter()

@router.get('/')
def home():
    return {"Welcome to the world !"}

@router.get('/clients', response_model=List[ClientOut])
def list_all_client(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.post('/clients', response_model=ClientOut, status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    if db.query(Client).filter(Client.email == client.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado !")
    if db.query(Client).filter(Client.cpf == client.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado !")

    new_client = Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

