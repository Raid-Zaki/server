from fastapi import UploadFile
from models.medias import UploadForm
from sqlalchemy.orm import Session

from models.users import User


class MediaController:
    
    @staticmethod
    async def  upload_media(data: UploadForm,user:User, db: Session,file:UploadFile):
        file_type =  file.content_type
        return file_type
        
