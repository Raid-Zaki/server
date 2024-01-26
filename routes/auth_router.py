from typing import Annotated
from fastapi import APIRouter, Depends, status
from controllers.auth_controller import AuthController
from database.connection import get_db
from forms.auth import LoginForm
from models.auth import Token

from models.user import User
from repositories.auth_repository import *
from responses.auth import SignUpResponse
router = APIRouter(tags=["users"])

@router.post("/login", response_model=Token)
async def login(form_data: LoginForm,db:Annotated[Session,Depends(get_db)]):
    return AuthController.login(user_data=form_data,db=db)

@router.get("/me", response_model=User)
async def user_info(user:Annotated[User,Depends(AuthRepository().get_current_user)]):
    return AuthController.user_info(user)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=SignUpResponse)
async def signup(user:SignUpForm,db:Annotated[Session,Depends(get_db)]):
    return AuthController.signup(user,db=db)
