from pydantic import BaseModel
import app.models.post_model  as modelpost

class PostCreate(BaseModel):
    title : str
    descrtiption:str
    post:str
    image_url: str
    song_url: str

class PostUpdate(BaseModel):
    title : str
    descrtiption:str
    post:str
    image_url: str
    song_url: str
    
class PostDelete(BaseModel):
    id:int

class PostRead(modelpost.Post):
    pass
