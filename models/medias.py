

from pydantic import BaseModel, model_validator
from typing import Annotated



from database.connection import get_db
from database.tables import MediaTypes
from pydantic import PositiveInt

class UploadForm (BaseModel):
    media_type_id: Annotated[int ,PositiveInt]
    title:str
    @model_validator(mode="after")
    def validate_media_type_id(self):
        db=next(get_db())
        media_type=db.query(MediaTypes).filter(MediaTypes.id==self.media_type_id).first()
        if media_type is None:
            raise ValueError("Media type does not exist")
        return self
        
    
class UserQuery(BaseModel):
    query:str 
    media_id:str
    
    
    
    
    
    