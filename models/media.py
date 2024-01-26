
from datetime import datetime

from pydantic import BaseModel

class Media(BaseModel):
    id: int
    user_id: str
    media_type_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
        
