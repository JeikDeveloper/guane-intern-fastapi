# Python
from datetime import datetime
from typing import Optional, List
from fastapi.param_functions import Depends

# pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic.networks import EmailStr

# Dogs
class DogsBase(BaseModel):
    name: str = Field(
        ...,
        min_length = 1,
        max_length = 20
    )
    picture: str = Field(
        ...
    )
    is_adopted: bool = Field(
        ...
    )
    create_date: datetime = Field(
        default = datetime.now()
    )
    id_user: Optional[int] = Field(
        default=None,
        ge=0
    )

    class Config:
        orm_mode = True


class Dogs(DogsBase):
    id: Optional[int]
    

## Modificar Dog
class DogsUpdate(BaseModel):   
    picture: str = Field(
        ...
    )
    is_adopted: bool = Field(
        ...
    )
    create_date: datetime = Field(
        default = datetime.now()
    )
    id_user: Optional[int] = Field(
        default=None,
        gt=0
    )
   
    class Config:
        orm_mode =True

## Mensajes de confirmación
class Respuesta(BaseModel):
    mensaje: str


# Users
class UserBase(BaseModel):
    name: str = Field(
        ...,
        min_length = 1,
        max_length = 40
    )
    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 40
    )
    email: str = Field(...)


class User(UserBase):
    id: Optional[int]
    dogs: List[Dogs] = []

    class Config:
        orm_mode =True

## Modificar User
class UserUpdate(BaseModel):   
    name: str = Field(
        ...,
        min_length = 1,
        max_length = 40
    )
    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 40
    )
    email: str = Field(...)
   
    class Config:
        orm_mode =True