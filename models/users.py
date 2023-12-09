
from typing import Annotated, Optional
from uuid import UUID
from pydantic import BaseModel, StringConstraints, model_validator,Field

class User(BaseModel):
    id: Optional[UUID]
    username: str
    email: str
    hashed_password: Optional[str]=Field(exclude=True)
    class Config:
        from_attributes = True
        
