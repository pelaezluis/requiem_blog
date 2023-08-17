from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from app.models.post_model import Post



class UserBase(SQLModel):
    __tablename__ = "users"

    id : Optional[int]=Field(default=None, primary_key=True,index=True,nullable=False)
    first_name : str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    username: str = Field(nullable=False, unique=True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    facebook_account: str
    instagram_accoutn:str
    created_at:Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    update_at: Optional[datetime] = Field(default=None, nullable=True)
    


    
class User(UserBase,table=True):
    posts:Post = Relationship(back_populates="user")
