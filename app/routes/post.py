from fastapi import APIRouter

router = APIRouter()


@router.get('')
async def get_posts():
    return {'posts': []}


@router.get('/{id}')
async def get_post():
    return {'post': 'post uno'}


@router.post('/create_user')
async def create_post():
    return {'post': 'created'}


@router.put('/update_post/{id}')
async def update_post(id: int):
    return {'status': 'updated'}


@router.delete('/delete_post/{id}')
async def delete_post(id: int):
    return {'status': 'deleted'}