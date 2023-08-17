from pydantic import BaseModel
from app.models.view_model import View
from datetime import datetime

class viewUpdate(BaseModel):
    last_view: datetime

class viewCreate(View):
    pass

class viewBasic(BaseModel):
    view_count: int
    last_view: datetime


class viewDelete(BaseModel):
    id: int


