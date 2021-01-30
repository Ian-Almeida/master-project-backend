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
        pass

class UserCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    active: bool

    class Config:
        str = Field(default_factory=uuid.uuid4, alias="_id") 

class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    active: Optional[bool]