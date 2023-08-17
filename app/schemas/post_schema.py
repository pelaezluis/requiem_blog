from pydantic import BaseModel
from app.models.post_model import Post
from datetime import datetime
from typing_extensions import Optional

    
class PostCreate(BaseModel):
    title : str
    description:str
    post:str
    image_url: str
    song_url: str
    




class PostUpdate(BaseModel):
    title : str
    description:str 
    post:str
    image_url: str
    song_url: str
    update_at: Optional[datetime] = None
    
    
class PostRead(Post):
    pass
