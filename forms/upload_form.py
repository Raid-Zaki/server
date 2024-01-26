

from pydantic import BaseModel, model_validator
from typing import Annotated



from database.connection import get_db
from database.tables import MediaTypes, Tasks
from pydantic import PositiveInt

class UploadForm (BaseModel):
    media_type_id: Annotated[int ,PositiveInt]
    title:str 
    task_id: Annotated[int ,PositiveInt]
    title:str
    @model_validator(mode="after")
    def validate_media_type_id(self):
        db=next(get_db())
        media_type=db.query(MediaTypes).filter(MediaTypes.id==self.media_type_id).first()
        task=db.query(Tasks).filter(Tasks.id==self.task_id).first()
        if media_type is None:
            raise ValueError("Media type does not exist")
        if task is None:
            raise ValueError("Task does not exist")
        return self