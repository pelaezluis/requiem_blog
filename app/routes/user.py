from fastapi import APIRouter

router = APIRouter()


@router.get('')
async def get_users():
    return {'users': []}


@router.get('/{id}')
async def get_user():
    return {'user': 'user uno'}


@router.post('/create_user')
async def create_user():
    return {'user': 'created'}


@router.put('/update_user/{id}')
async def update_user(id: int):
    return {'status': 'updated'}


@router.delete('/delete_user/{id}')
async def delete_user(id: int):
    return {'status': 'deleted'}