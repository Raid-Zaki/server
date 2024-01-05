from fastapi import UploadFile
from fastapi.responses import JSONResponse
from models.medias import UploadForm, UserQuery
from sqlalchemy.orm import Session
from models.users import User
from repositories.vector_repository import VectorRepository


class MediaController:
    
    @staticmethod
    async def  upload_media(data: UploadForm,user:User, db: Session,file:UploadFile):
        vector_repo= VectorRepository(file,user)
        media_id = await vector_repo.embedd(db=db,data=data)

        return JSONResponse({"media_id": str(media_id)},background=vector_repo.delete_temp_file)
       
    @staticmethod
    async def query(query:UserQuery,user:User,db:Session):
       
        return await VectorRepository.query(query,user,db)
        
