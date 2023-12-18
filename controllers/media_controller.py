from fastapi import UploadFile
from models.medias import UploadForm
from sqlalchemy.orm import Session

from models.users import User
from services.embedder import Embedder


class MediaController:
    
    @staticmethod
    async def  upload_media(data: UploadForm,user:User, db: Session,file:UploadFile):
    
        embedder=await Embedder(file)
        return embedder.embedd()
        
