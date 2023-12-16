from typing import Optional
from uuid import UUID

from pydantic import BaseModel



class Post(BaseModel):
    """The post model."""
    id: Optional[UUID]
    title: str
    description: str
    class Config:
        from_attributes = True

class DeletePostResponse(BaseModel):
    detail: str

class UpdatePost(BaseModel):
    id: UUID
    title: str
    description: str

    class Config:
        from_attributes = True
