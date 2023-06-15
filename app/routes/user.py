from fastapi import APIRouter, HTTPException,Depends
# import app.schemas.user_schema as UserSchema, tenias esta
from app.schemas.user_schema import UserBasic, UserCreate, UserRead, UserUpdate
from app.seguridad.seguridad_login import get_current_user,  get_password_hash
from app.user_data import users


router = APIRouter()

# Ruta para crear un usuario
@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    user_id = max(users.keys()) + 1
    user_data = user.dict(exclude_unset=True)
    hashed_password = get_password_hash(user_data["password"])
    user_data["password"] = hashed_password
    new_user = UserRead(id=user_id, **user_data)
    users[user_id] = new_user
    print(new_user)
    return new_user

@router.get("/users/{user_id}", response_model=UserBasic)
def get_user(user_id: int, current_user: UserRead = Depends(get_current_user)):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Obtener una lista de usuarios
@router.get("/users", response_model=list[UserBasic])
def get_users(current_user: UserRead = Depends(get_current_user)):
    return list(users.values())

@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate,current_user: UserRead = Depends(get_current_user)):
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
def delete_user(user_id: int, current_user: UserRead = Depends(get_current_user)):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return user