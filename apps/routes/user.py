from fastapi import APIRouter, Body, Request, HTTPException, status, FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
import os
import hashlib
from apps.models.users import UserCreateModel, UserModel, UpdateUserModel, UserLogin

router = APIRouter()

# @router.get("/")
# async def 

@router.get("/login/{email}/{password}", response_description="Login user")
async def check_user(
    request: Request,
    email: EmailStr,
    password: str
):
    searched_user = await request.app.mongodb["user"].find_one(
        {"email": email}
    )

    if not searched_user:
            raise HTTPException(status_code=404, detail=f"User {email} not found")

    user_password = {
        'salt': searched_user['password'][:32],
        'key': searched_user['password'][32:]
    }

    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user_password['salt'], 100000)

    if key != user_password['key']:
        return {
            'error': 'Invalid password',
            'status': 400,
            'valid': False 
        }
    else:
        return {
            'error': None,
            'status': 200,
            'valid': True
        }

@router.post("/signup", response_description="Create user")
async def create_user(
    request: Request,
    user: UserCreateModel = Body(...)
):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', user.password.encode('utf-8'), salt, 100000)

    hashed_password = salt + key

    searched_user = await request.app.mongodb["user"].find_one(
        {"email": user.email}
    )

    if not searched_user:
        user = jsonable_encoder(user)
        user['password'] = hashed_password
        new_user = await request.app.mongodb["user"].insert_one(user)
        created_user = await request.app.mongodb["user"].find_one(
            {"_id": new_user.inserted_id}
        )
        return signJWT(user["email"])
    else:
        raise HTTPException(status_code=400, detail=f"User {searched_user['email']} already exists")