from fastapi import UploadFile
from fastapi.responses import JSONResponse
from models.medias import UploadForm
from sqlalchemy.orm import Session

from models.users import User
from repositories.vector_repository import VectorRepository


class MediaController:
    
    @staticmethod
    async def  upload_media(data: UploadForm,user:User, db: Session,file:UploadFile):
        vecotor_repo= VectorRepository(file,user)
        await vecotor_repo.embedd()
        return JSONResponse({"status":"ok"},background=vecotor_repo.delete_temp_file)
       
        
