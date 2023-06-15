from passlib.context import CryptContext
from app.user_data import users
from fastapi import HTTPException
from datetime import timedelta, datetime
from typing import Optional
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from app.schemas.user_schema import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

SECRET_KEY = "0f42f37161dcb7500f70887898c55e39d46c3d94da7da9995211a3caa410fb73"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str):
    user = None
    print("entra")
    for user_id, user_data in users.items():
        print(user_data)
        if user_data.email == email:
            print("bien")
            user = user_data
            break

    if user is None:
        print("User not found")
        return None
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    print(user)
    return user

    """
    user_data = {"sub": user.email, "username": user.username}
    access_token = create_access_token(user_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return access_token"""
    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        print("token",token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload", payload)
        username = payload.get("sub")
        print("username", username)
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = None
    for user_id, user_data in users.items():
        if user_data.username == username:
            user = user_data
            break

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user