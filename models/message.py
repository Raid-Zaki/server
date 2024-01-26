from datetime import datetime
from pydantic import BaseModel

class Message(BaseModel):
    id: int
    chat_id: int
    human_question: str
    bot_answer: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
        
