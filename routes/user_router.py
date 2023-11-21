

from datetime import timedelta
from typing import Annotated,Dict

from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database.connection import get_db
from models.users import Token, User, UserSignUp
from utils.user_auth import *

router = APIRouter(tags=["users"])
@router.post("/login/username", response_model=Token)
async def login_by_username(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)
):
    user = authenticate_user_by_username(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)
@router.get("/me", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSignUp)
async def signup(user: UserForm, db: Session = Depends(get_db)):
    user= create_user(db=db, user=user)
    access_token=create_access_token(data={"sub": user.username})
    return UserSignUp(user=user,token=Token(access_token=access_token))
    