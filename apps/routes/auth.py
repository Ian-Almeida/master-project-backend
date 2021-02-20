from typing import Any
from fastapi import APIRouter, Body, Request, HTTPException, status, FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
import os
import hashlib
from apps.models.auth import Token

router = APIRouter()

@router.post('/token') 
async def verify_token(
    token: Token,
) -> Any:

    verification = JWTBearer.verify_jwt(JWTBearer, jwtoken=token.access_token)

    if not verification:
        raise HTTPException(status_code=401, detail=f"Token unauthorized")

    return verification;