from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, status,Form
from controllers.media_controller import MediaController
from database.connection import get_db

from pydantic import  Json
from sqlalchemy.orm import Session
from forms.chat_query import ChatQuery
from forms.upload_form import UploadForm
from models.user import User
from repositories.auth_repository import AuthRepository

router = APIRouter(tags=["medias"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_media(data:Annotated[Json[UploadForm], Form()],db: Annotated[Session, Depends(get_db)],user:Annotated[User,Depends(AuthRepository().get_current_user)],file: UploadFile = None ):
    result= await MediaController.upload_media(data=data,db=db,user=user,file=file)
    return result
@router.post("/query",status_code=status.HTTP_201_CREATED)
async def query(query:ChatQuery, db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(AuthRepository().get_current_user)]):
    return await  MediaController.query(query=query,db=db,user=user)