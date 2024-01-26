from sqlalchemy import func
from database.tables import Chats, Messages, Users
from forms.chat_query import ChatQuery
from sqlalchemy.orm import Session
from models.user import User
from repositories.chat_repository import ChatRepository
from typing import Annotated
from fastapi_pagination import paginate
from responses.chat import ChatResponse

from fastapi_pagination.ext.sqlalchemy import paginate

from models.message import Message


class ChatController:
    
       
    @staticmethod
    async def query(query:ChatQuery,id:int,db:Session):
        return await ChatRepository.resolve_chat_query(query,id,db)
    @staticmethod
    async def history(user:User,db:Session):
        user=db.query(Users).filter(Users.id==user.id).first()
        return paginate(db.query(Chats).filter(Chats.user==user).order_by(Chats.updated_at.desc()),transformer=ChatController.__chat_transformer)
     
        
    
    @staticmethod
    def __chat_transformer(chats:list[Chats]):
        result=[]
        for chat in chats:
            if len(chat.messages):
                    latest_message=Message.model_validate(chat.messages[0])
            else:
                latest_message=None
            chat=ChatResponse(id=chat.id,title=chat.media.title,task=chat.task.name,media_type=chat.media.mediaType.name,created_at=chat.created_at,updated_at=chat.updated_at,lastest_message=latest_message)
            result.append(chat)
        return result
    
    @staticmethod 
    def __message_transformer(messages:list[Messages]):
        result=[]
        for message in messages:
            message=Message.model_validate(message)
            result.append(message)
        return result
    
    
    @staticmethod 
    async def chat_history(user:User,db:Session,id:int):
        chat=db.query(Chats).filter(Chats.id==id).first()
        if chat and chat.media.user_id==user.id:
            return paginate(db.query(Messages).filter(Messages.chat_id==id).order_by(Messages.created_at.desc()),transformer=ChatController.__message_transformer)
        else:
            return None
       
 
        
