from pydantic import BaseModel
import models.view_model  as modelview

class viewUpdate(BaseModel):
    view_count: int


class viewDelete(BaseModel):
    id: int


