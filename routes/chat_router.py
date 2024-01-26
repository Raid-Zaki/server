from typing import Annotated

from fastapi import APIRouter, Depends
from controllers.chat_controller import ChatController
from database.connection import get_db
from forms.chat_query import ChatQuery
from sqlalchemy.orm import Session

from models.user import User
from repositories.auth_repository import AuthRepository

router=APIRouter(tags=["chats"])
@router.post('/{id}')
async def user_query(chatQuery:ChatQuery,db:Annotated[Session,Depends(get_db)],id:int,user:Annotated[User,Depends(AuthRepository().get_current_user)]):

    return await ChatController.query(chatQuery,id,db)

