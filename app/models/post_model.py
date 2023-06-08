
from sqlmodel import SQLModel,Field, Relationship
from typing import Optional
from datetime import datetime


class PostBase(SQLModel, table=True):
    __tablename__ = "posts"
    id : Optional[int]=Field(default=None, primary_key=True,index=True,nullable=False)
    user_id: int = Field(foreign_key="users.id")
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    post: str = Field(nullable=False)
    image_url: str = Field(nullable=False)
    song_url: str = Field(nullable=False)
    created_at:Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    update_at: Optional[datetime] = Field(default=None, nullable=True)



class Post(PostBase):
    user:"User" = Relationship(back_populates="posts")
    view :"View"= Relationship(back_populates="posts")
    
