from fastapi import UploadFile
from fastapi.responses import JSONResponse
from database.tables import Chats
from forms.chat_query import ChatQuery
from sqlalchemy.orm import Session
from forms.upload_form import UploadForm
from models.chat import Chat

from models.user import User
from repositories.vector_repository import VectorRepository


class MediaController:
    
    @staticmethod
    async def  upload_media(data: UploadForm,user:User, db: Session,file:UploadFile):
        vecotor_repo= VectorRepository(file,user)
        result=await vecotor_repo.embedd(db=db,data=data)
        chat=Chats(media_id=result.id,task_id=data.task_id)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        media_title=chat.media.title
        task_name=chat.task.name
        title=media_title+"-"+task_name
        chat=Chat.model_validate(chat)
        return JSONResponse({**chat.model_dump(),"title":title},background=vecotor_repo.delete_temp_file)
       
    @staticmethod
    async def query(query:ChatQuery,user:User,db:Session):
       
        return await VectorRepository.query(query,user,db)
        
