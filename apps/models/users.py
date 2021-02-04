from typing import Optional
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
import uuid

class UserModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    active: bool

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "My name",
                "email": "myemail@email.com",
                "password": "secretpassword123",
                "active": True,
            }
        }

class UserCreateModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    active: bool

    class Config:
        str = Field(default_factory=uuid.uuid4, alias="_id") 

class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    isAuthUser: bool

class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    active: Optional[bool]