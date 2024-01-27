from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from controllers.chat_controller import ChatController
from database.connection import get_db
from forms.chat_query import ChatQuery
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from models.chat import Chat
from models.user import User
from repositories.auth_repository import AuthRepository
from responses.chat import ChatResponse
from fastapi_pagination.links import Page
from models.message import Message

router=APIRouter(tags=["chats"])
@router.post('/{id}',response_model=Message)
async def user_query(chatQuery:ChatQuery,db:Annotated[Session,Depends(get_db)],id:int,user:Annotated[User,Depends(AuthRepository().get_current_user)]):

    return await ChatController.query(chatQuery,id,db)

@router.get('/',response_model=Page[ChatResponse])
async def user_chats(user:Annotated[User,Depends(AuthRepository().get_current_user)],db:Annotated[Session,Depends(get_db)]):

    return await ChatController.history(user,db)

@router.get('/{id}',response_model=Page[Message])
async def chat_history(user:Annotated[User,Depends(AuthRepository().get_current_user)],db:Annotated[Session,Depends(get_db)],id:int):

    result= await ChatController.chat_history(user,db,id)
    if result!=None:
        return result
    
    raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

