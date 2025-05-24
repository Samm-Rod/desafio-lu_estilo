from pydantic import BaseModel, EmailStr, constr
from app.models.client_entity import Client


class ClientBase (BaseModel):
    name: str
    email: EmailStr
    cpf: constr(min_length=11, max_length=11)

class ClientCreate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True