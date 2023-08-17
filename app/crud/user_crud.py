from sqlmodel import Session, select
from app.models.user_model import User
from datetime import datetime
from typing_extensions import List, Optional
from app.schemas.user_schema import UserCreate, UserUpdate

def check_existing_user(db:Session,email: str, username: str) -> bool:
    existing_email = db.exec(select(User).where(User.email == email)).first()
    if existing_email:
        return True
    existing_username = db.exec(select(User).where(User.username == username)).first()
    if existing_username:
        return True
    return False


def get_user_by_email(db:Session, email:str):
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    return user

def get_user_by_username(db:Session, username:str):
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    return user

def get_users(db:Session) -> List[User]:
    statement = select(User)
    users = db.exec(statement).all()
    return users

def get_user_by_id(db:Session,user_id: int) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()
    return user

def create_user(db:Session,user: UserCreate) -> User:
    from app.seguridad.seguridad_login import get_password_hash
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    db_user = User.from_orm(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db:Session,user_id: int, user: UserUpdate) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    db_user = db.exec(statement).first()
    if db_user:
        for field, value in user.dict(exclude_unset=True).items():
            setattr(db_user, field, value)
        db_user.update_at = datetime.utcnow() # Actualiza la columna update_at con la fecha y hora actuales
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db:Session,user_id: int) -> bool:
        statement = select(User).where(User.id == user_id)
        db_user = db.exec(statement).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False