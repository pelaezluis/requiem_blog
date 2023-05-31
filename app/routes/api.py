from fastapi import APIRouter
from app.routes import user, post

router = APIRouter()

router.include_router(user.router, prefix='/user', tags=['User'])
router.include_router(post.router, prefix='/post', tags=['Post'])