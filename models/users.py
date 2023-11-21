
from typing import Annotated, Optional
from uuid import UUID
from pydantic import BaseModel, StringConstraints, model_validator,Field
class Token(BaseModel):
    access_token: str
  
class TokenData(BaseModel):
    username: str | None = None

class UserForm(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True,min_length=3, max_length=50)]
    email: Annotated[str,StringConstraints(strip_whitespace=True, pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')]
    full_name:  Annotated[str, StringConstraints(strip_whitespace=True,min_length=3, max_length=50,pattern=r'^[a-zA-Z]+ [a-zA-Z]+$')]
    password: Optional[str]
    password_confirmation: Optional[str]
    class Config:
        from_attributes = True
    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password and self.password_confirmation and self.password != self.password_confirmation:
            raise ValueError('Passwords do not match')
        return self
class User(BaseModel):
    id: Optional[UUID]
    
    username: str
    email: str
    full_name: str
    hashed_password: Optional[str]=Field(exclude=True)
    class Config:
        from_attributes = True
        
class UserSignUp(BaseModel):
    user:User 
    token:Token