from fastapi import APIRouter

from app.api.v1 import route_authenticated, route_users, question


api_router = APIRouter()
api_router.include_router(route_users.router, prefix='/users', tags=['Users'])
api_router.include_router(route_authenticated.router, prefix='', tags=['Authentication'])
api_router.include_router(question.router, prefix="/questions", tags=["Questions"])
