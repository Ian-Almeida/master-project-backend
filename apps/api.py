from fastapi import APIRouter

from apps.routes import routers
from apps.routes import user

api_router = APIRouter()

api_router.include_router(routers.router, prefix="/routers", tags=["routers"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
