from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from controllers.auth_controller import AuthController
from database.connection import get_db
from models.users import Token, User, UserSignUpResponse
from repositories.auth_repository import *
router = APIRouter(tags=["users"])

@router.post("/login/username", response_model=Token)
async def login_by_username(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Annotated[Session,Depends(get_db)]):
    return AuthController.login_by_username(form_data=form_data,db=db)

@router.get("/me", response_model=User)
async def user_info(user:Annotated[User,Depends(AuthRepository().get_current_user)]):
    return AuthController.user_info(user)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSignUpResponse)
async def signup(user:UserForm,db:Annotated[Session,Depends(get_db)]):
    return AuthController.signup(user,db=db)
