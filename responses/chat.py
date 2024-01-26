from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from models.message import Message

class ChatResponse(BaseModel):
    id:int 
    title:str
    task:str
    created_at:datetime
    lastest_message:Optional[Message|list[Message]]=None
    