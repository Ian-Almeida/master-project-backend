from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    _id: Optional[str] = None
