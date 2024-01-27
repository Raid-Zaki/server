from typing import  Optional
from pydantic import BaseModel,model_validator
from enum import Enum


class Language(str, Enum):
    english = 'en'
    arabic = 'ar'

class ChatQuery(BaseModel):
    query:Optional[str]=None
    target_language:Language=Language.arabic
    source_language:Language=Language.english
    
    @model_validator(mode="after")
    def validate_language_sanity(self):
        if self.source_language == self.target_language:
            raise ValueError('Source and target languages must be different')
        return self
    

    
    
    
    