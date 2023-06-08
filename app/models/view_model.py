from sqlmodel import SQLModel, Relationship, Field
from datetime import datetime
from typing import Optional
from .post_model import Post

class ViewBase(SQLModel):
    __tablename__ = "views"

    id:Optional[int]=Field(default=None, primary_key=True,index=True,nullable=False)
    view_count: int = Field(nullable=False)
    post_id: int= Field(foreign_key="posts.id")
    last_view : Optional[datetime] = Field(default=None, nullable=True)

class View(ViewBase):
    post:Post = Relationship( back_populates="view")



