from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config.config import settings
import os
from starlette.middleware.cors import CORSMiddleware

from apps.api import api_router

SECRET = "a3a0361bd9d72bd52aa6853131205753fa6afb8e03dc23e1"

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(api_router, prefix=settings.API_STR)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
