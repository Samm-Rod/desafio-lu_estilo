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


@router.get('/clients/{client_id}', response_model=ClientOut)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado !")
    return client


@router.put('/clients/{client_id}', response_model=ClientOut)
def update_client(client_id: int, client_data: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado !")

    # Verifica se o novo email ou CPF já estão em uso por outro cliente
    if db.query(Client).filter(Client.email == client_data.email, Client.id != client_id).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado por outro cliente!")
    if db.query(Client).filter(Client.cpf == client_data.cpf, Client.id != client_id).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado por outro cliente!")

    # Atualiza os campos
    for field, value in client_data.dict().items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)

    return client


@router.delete('/clients/{client_id}')
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado !")

    db.delete(client)
    db.commit()

    return {"message": "Cliente deletado com sucesso!"}