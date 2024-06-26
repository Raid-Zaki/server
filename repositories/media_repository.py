from database.tables import Medias
from forms.upload_form import UploadForm
from models.user import User
from sqlalchemy.orm import Session

class MediaRepository:
    
    @staticmethod 
    def create(data:UploadForm,user:User,db:Session)->Medias:
        media=Medias()
        media.title=data.title
        media.media_type_id=data.media_type_id
        media.user_id=user.id
        db.add(media)
        db.commit()
        db.refresh(media)
        return  media