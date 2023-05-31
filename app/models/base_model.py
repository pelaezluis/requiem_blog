from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field


class Base(BaseModel):
    id: int
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)