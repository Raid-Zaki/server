from datetime import timedelta
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from forms.auth import LoginForm, SignUpForm
from models.auth import Token

from models.user import User
from repositories.auth_repository import AuthRepository
from responses.auth import SignUpResponse, LoginResponse
class AuthController:
    auth_repository=AuthRepository()
    @staticmethod
    def login(user_data: LoginForm,db: Session ):
        user = AuthController.auth_repository.authenticate_user(db, user_data.cred, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=AuthController.auth_repository.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthController.auth_repository.create_access_token(
            data={"sub": user_data.cred}, expires_delta=access_token_expires
        )
        return LoginResponse(token=Token(access_token=access_token), user=user)
    
    @staticmethod
    def signup(user: SignUpForm, db: Session ):
        user= AuthController.auth_repository.create_user(db=db, user=user)
        access_token=AuthController.auth_repository.create_access_token(data={"sub": user.email})
        return SignUpResponse(user=user,token=Token(access_token=access_token))
    
    @staticmethod
    def user_info(current_user: User):
        return current_user