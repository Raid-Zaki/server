from typing import Annotated
from fastapi import APIRouter, Depends, status

from database.connection import get_db
from sqlalchemy.orm import Session
from database.tables import Users

from repositories.auth_repository import AuthRepository
router = APIRouter(tags=["test"])

@router.get("/me")
async def test(db:Annotated[Session,Depends(get_db)],user:Annotated[Users,Depends(AuthRepository().get_current_user)]):
    return user.chats
    
    
