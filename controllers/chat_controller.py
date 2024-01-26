from database.tables import Chats, Users
from forms.chat_query import ChatQuery
from sqlalchemy.orm import Session
from models.user import User
from repositories.chat_repository import ChatRepository
from typing import Annotated
from fastapi_pagination import paginate
from responses.chat import ChatResponse

from models.message import Message


class ChatController:
    
       
    @staticmethod
    async def query(query:ChatQuery,id:int,db:Session):
        return await ChatRepository.resolve_chat_query(query,id,db)
    @staticmethod
    async def history(user:User,db:Session):
        user=db.query(Users).filter(Users.id==user.id).first()
        chats=user.chats
        result=[]
        for i in chats:
            if len(i.messages):
                latest_message=Message.model_validate(i.messages[0])
            else:
                latest_message=None
            i=ChatResponse(id=i.id,title=i.media.title,task=i.task.name,media_type=i.media.mediaType.name,created_at=i.created_at,updated_at=i.updated_at,lastest_message=latest_message)
            result.append(i)
        return result
    
    
    @staticmethod 
    
    async def chat_history(user:User,db:Session,id:int):
        chat=db.query(Chats).filter(Chats.id==id).first()
        if chat:
            if chat.media.user_id==user.id:
                messages=chat.messages
                result=[]
                for i in messages:
                    i=Message.model_validate(i)
                    result.append(i)
                return result
            else:
                return None
        else:
            return None
       
 
        
