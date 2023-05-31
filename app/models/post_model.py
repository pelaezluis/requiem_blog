from pydantic import BaseModel
from sqlmodel import SQLModel

class PostBase(SQLModel):
    user_id: int
    title: str
    description: str
    post: str
    image_url: str
    song_url: str