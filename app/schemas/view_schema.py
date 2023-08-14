from pydantic import BaseModel
from app.models.view_model import View

class viewUpdate(BaseModel):
    view_count: int

class viewCreate(View):
    pass

class viewBasic(BaseModel):
    post_id:int
    view_count: int

class viewDelete(BaseModel):
    id: int


