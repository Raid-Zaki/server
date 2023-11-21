from datetime import timedelta
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.users import Token, User, UserForm, UserSignUpResponse
from repositories.auth_repository import AuthRepository
class AuthController:
    auth_repository=AuthRepository()
    @staticmethod
    def login_by_username(form_data: OAuth2PasswordRequestForm,db: Session ):
        user = AuthController.auth_repository.authenticate_user_by_username(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=AuthController.auth_repository.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthController.auth_repository.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token)
    @staticmethod
    def signup(user: UserForm, db: Session ):
        user= AuthController.auth_repository.create_user(db=db, user=user)
        access_token=AuthController.auth_repository.create_access_token(data={"sub": user.username})
        return UserSignUpResponse(user=user,token=Token(access_token=access_token))
    @staticmethod
    
    
    def user_info(current_user: User):
        return current_user