
from datetime import datetime
from typing import  Optional
from pydantic import BaseModel,Field

class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: Optional[str]=Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
        
