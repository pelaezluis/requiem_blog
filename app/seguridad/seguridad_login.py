from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import timedelta, datetime
from typing import Optional
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from app.schemas.user_schema import TokenData
from sqlmodel import Session
from app.database.database import engine
from app.crud.user_crud import get_user_by_username
from app.models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/access")

SECRET_KEY = "0f42f37161dcb7500f70887898c55e39d46c3d94da7da9995211a3caa410fb73"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_db():
    db = Session(engine)
    try: 
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db:Session, username: str, password: str):
    print("entra a la autenticathe"   )
    user = get_user_by_username(db,username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect User")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    db.add(user)
    db.commit()
    return user
    

    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db,username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

