from typing import Annotated, Optional
from pydantic import BaseModel, StringConstraints, model_validator
class SignUpForm(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True,min_length=3, max_length=50)]
    email: Annotated[str,StringConstraints(strip_whitespace=True, pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')]
    password: Optional[str]
    password_confirmation: Optional[str]
    class Config:
        from_attributes = True
    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password and self.password_confirmation and self.password != self.password_confirmation:
            raise ValueError('Passwords do not match')
        return self
class LoginForm(BaseModel):
    cred: str
    password: str
    class Config:
        from_attributes = True