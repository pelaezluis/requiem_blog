from fastapi import APIRouter, HTTPException
import schemas.user_schema as UserSchema



router = APIRouter()

# Diccionario ficticio de usuarios
users = {
    1: UserSchema.UserRead(id=1, first_name="John", last_name="Doe", email="john.doe@example.com", username="johndoe", password="password123", facebook_account="john.doe", instagram_accoutn="john.doe"),
    2: UserSchema.UserRead(id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com", username="janedoe", password="password123", facebook_account="jane.doe", instagram_accoutn="jane.doe"),
}

# Ruta para crear un usuario
@router.post("/users", response_model=UserSchema.UserRead)
def create_user(user: UserSchema.UserCreate):
    user_id = max(users.keys()) + 1
    user_data = user.dict(exclude_unset=True)
    new_user = UserSchema.UserRead(id=user_id, **user_data)
    users[user_id] = new_user
    return new_user

@router.get("/users/{user_id}", response_model=UserSchema.UserBasic)
def get_user(user_id: int):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Obtener una lista de usuarios
@router.get("/users", response_model=list[UserSchema.UserBasic])
def get_users():
    return list(users.values())

@router.put("/users/{user_id}", response_model=UserSchema.UserRead)
def update_user(user_id: int, user_update: UserSchema.UserUpdate):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.dict()
    updated_user_data = user_update.dict(exclude_unset=True)
    user_data.update(updated_user_data)

    updated_user = UserSchema.UserRead(**user_data)
    users[user_id] = updated_user
    return updated_user

# Ruta para eliminar un usuario
@router.delete("/users/{user_id}", response_model=UserSchema.UserRead)
def delete_user(user_id: int):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return user