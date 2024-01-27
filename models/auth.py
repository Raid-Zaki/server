from typing import  Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
  
class TokenData(BaseModel):
    cred:Optional[str]
    



    
