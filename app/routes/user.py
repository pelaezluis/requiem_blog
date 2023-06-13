from fastapi import APIRouter, HTTPException
# import app.schemas.user_schema as UserSchema, tenias esta
from app.schemas.user_schema import UserBasic, UserCreate, UserRead, UserUpdate



router = APIRouter()

# Diccionario ficticio de usuarios
users = {
    1: UserRead(id=1, first_name="John", last_name="Doe", email="john.doe@example.com", username="johndoe", password="password123", facebook_account="john.doe", instagram_accoutn="john.doe"),
    2: UserRead(id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com", username="janedoe", password="password123", facebook_account="jane.doe", instagram_accoutn="jane.doe"),
}

# Ruta para crear un usuario
@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    user_id = max(users.keys()) + 1
    user_data = user.dict(exclude_unset=True)
    new_user = UserRead(id=user_id, **user_data)
    users[user_id] = new_user
    return new_user

@router.get("/users/{user_id}", response_model=UserBasic)
def get_user(user_id: int):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Obtener una lista de usuarios
@router.get("/users", response_model=list[UserBasic])
def get_users():
    return list(users.values())

@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.dict()
    updated_user_data = user_update.dict(exclude_unset=True)
    user_data.update(updated_user_data)

    updated_user = UserRead(**user_data)
    users[user_id] = updated_user
    return updated_user

# Ruta para eliminar un usuario
@router.delete("/users/{user_id}", response_model=UserRead)
def delete_user(user_id: int):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return user