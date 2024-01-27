from typing import Optional
from pydantic import BaseModel


class ChatQuery(BaseModel):
    query:Optional[str]=None
    
    
    