
from datetime import datetime
from typing import  Optional
from pydantic import BaseModel,Field

class Taks(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
        
