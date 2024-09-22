from pydantic import BaseModel
from datetime import datetime

class PartBase(BaseModel):
    id: int
    row_part: str
    col_part: str
    changeover_time: float

class PartCreate(PartBase):
    pass

class Part(PartBase):
    id: int

    class Config:
        orm_mode = True
