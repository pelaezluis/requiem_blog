from fastapi import APIRouter
from . import user, post,login

api_router = APIRouter()

api_router.include_router(user.router, prefix='/user', tags=['User'])
api_router.include_router(post.router, prefix='/post', tags=['Post'])
api_router.include_router(login.router, tags=['Login'])