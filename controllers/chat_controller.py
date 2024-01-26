from forms.chat_query import ChatQuery
from sqlalchemy.orm import Session
from repositories.chat_repository import ChatRepository


class ChatController:
    
       
    @staticmethod
    async def query(query:ChatQuery,id:int,db:Session):
        return await ChatRepository.resolve_chat_query(query,id,db)
    
 
        
