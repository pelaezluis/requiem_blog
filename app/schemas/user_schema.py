from pydantic import BaseModel
from typing import Union

from models.user_model import User


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
