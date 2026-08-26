from app.api.v1 import route_authenticated
from fastapi import APIRouter

from app.api.v1 import route_users

api_router = APIRouter()
api_router.include_router(route_users.router, prefix='/user', tags=['user'])
api_router.include_router(route_authenticated.router, prefix='', tags=['login_and_logout'])
