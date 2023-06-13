from fastapi import APIRouter
from app.routes import user, post

api_router = APIRouter()

api_router.include_router(user.router, prefix='/user', tags=['User'])
api_router.include_router(post.router, prefix='/post', tags=['Post'])