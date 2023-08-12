from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import LoginData, Token
from app.seguridad.seguridad_login import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

@router.post("/access", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print("Access token created:", access_token)
    return {"access_token": access_token, "token_type": "bearer"}

"""
@router.post("/access", response_model=Token)
def login_for_access_token(form_data: LoginData = Body(...)):
    print("entra a la ruta de luis")
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    print("Access token created:", access_token)
    return {"access_token": access_token, "token_type": "bearer"}"""