from pydantic import BaseModel
from models.auth import Token
from models.user import User




class SignUpResponse(BaseModel):
    user:User 
    token:Token