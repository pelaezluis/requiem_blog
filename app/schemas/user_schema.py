from pydantic import BaseModel
from typing import Union

from app.models.user_model import User


class UserBasic(BaseModel):
    email: str
    first_name: str
    last_name:str
    email: str
    facebook_account: str
    instagram_accoutn:str
    username: str



class UserCreate(UserBasic):
    password: str
    

class UserUpdate(BaseModel):
    first_name: str
    last_name:str
    email: str
    facebook_account: str
    instagram_accoutn:str
    username: str

class UserRead(User):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str,None] = None

### agregé esto
class LoginData(BaseModel):
    username: str
    password: str