
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import  BaseModel, field_serializer

class Chat(BaseModel):
    id: int
    media_id: Optional[UUID]=None
    task_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
    @field_serializer('media_id')
    def serialize_uuid(self, media_id: UUID):
        return media_id.__str__()
    
    @field_serializer('created_at','updated_at')
    def serialize_dt(self, dt: datetime):
        return dt.timestamp()
    
        
