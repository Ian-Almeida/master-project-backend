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

@router.get("/", response_description="Get all users")
async def get_all_users(request: Request):
    users = []
    for user in await request.app.mongodb["user"].find().to_list(length=100):
        user['password'] = ''
        users.append(user)
    return users

@router.post("/login", response_description="Login user")
async def check_user(
    request: Request,
    login_user: UserLogin,
):
    searched_user = await request.app.mongodb["user"].find(
        {"email": login_user.email}
    ).to_list(length=100)

    if not searched_user:
            raise HTTPException(status_code=404, detail=f"User {login_user.email} not found")

    user_password = {
        'salt': searched_user[0]['password'][:32],
        'key': searched_user[0]['password'][32:]
    }

    key = hashlib.pbkdf2_hmac('sha256', login_user.password.encode('utf-8'), user_password['salt'], 100000)
    del searched_user[0]['password']
    
    if key != user_password['key']:
        raise HTTPException(status_code=400, detail=f"Invalid login!")
    else:
        return [{
            'data': searched_user,
            'isAuthUser': True,
            'error': None,
            'status': 200,
            'valid': True,
            'authKey': signJWT(searched_user[0]['_id'])
        }]

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

        await request.app.mongodb["user"].insert_one(user)
        created_user = await request.app.mongodb["user"].find(
            {"email": user['email']}
        ).to_list(length=100)
        created_user[0]['token'] = signJWT(created_user[0]['_id'])
        del created_user[0]['password']

        return [created_user[0]]
    else:
        raise HTTPException(status_code=400, detail=f"User {searched_user['email']} already exists")