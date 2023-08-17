from fastapi import APIRouter, HTTPException,Depends
# import app.schemas.user_schema as UserSchema, tenias esta
from app.schemas.user_schema import UserBasic, UserCreate, UserRead, UserUpdate
from app.seguridad.seguridad_login import get_current_user
from sqlmodel import Session
from app.database.database import engine
import app.crud.user_crud as crud


router = APIRouter()

def get_db():
    db = Session(engine)
    try: 
        yield db
    finally:
        db.close()

# Ruta para crear un usuario
@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db:Session= Depends(get_db)):
    if crud.check_existing_user(db,user.email, user.username):
        raise  HTTPException(status_code=409, detail="Email or username already registered")
    return crud.create_user(db,user)



#obtener solo un usuario por id
@router.get("/users/{user_id}", response_model=UserBasic)
def get_user(user_id: int, current_user: UserRead = Depends(get_current_user), db:Session= Depends(get_db)):
    user= crud.get_user_by_id(db,user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Obtener una lista de usuarios
@router.get("/users", response_model=list[UserRead])
def get_users(current_user: UserRead = Depends(get_current_user), db:Session=Depends(get_db)):
    users = crud.get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="not user existing")
    return users

#actualizar un usuario
@router.put("/users/{user_id}", response_model=UserBasic)
def update_user(user_id: int, user_update: UserUpdate,current_user: UserRead = Depends(get_current_user), db:Session=Depends(get_db)):
    user = crud.get_user_by_id(db,user_id)
    if crud.check_existing_user(db,user_update.email, user_update.username):
        raise  HTTPException(status_code=409, detail="Email or username already registered")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_user = crud.update_user(db,user_id, user_update)
    return update_user


# Ruta para eliminar un usuario
@router.delete("/users/{user_id}")
def delete_user(user_id: int, current_user: UserRead = Depends(get_current_user), db:Session=Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}