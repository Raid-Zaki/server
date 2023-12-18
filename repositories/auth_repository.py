from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import dotenv
import os
from sqlalchemy.orm import Session
from database.connection import get_db
from database.tables import Users
from models.auth import SignUpForm, TokenData
from utils.form_helper import FormHelper


class AuthRepository:
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    def __init__(self)->None:
        dotenv.load_dotenv()
        self.__SECRET_KEY = os.getenv("SECRET_KEY")
        self.__ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30*30
    
    def verify_password(self,plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    def get_password_hash(self,password):
        return self.pwd_context.hash(password)
    def get_user_by_username(self,db:Session, username: str):
        return db.query(Users).filter(Users.username == username).first()
    def get_user_by_email(self,db:Session, email: str):
        return db.query(Users).filter(Users.email == email).first()
    
    
    
    def authenticate_user(self,db:Session, cred: str, password: str):
        if FormHelper.is_valid_email(cred):
            user = self.get_user_by_email(db, cred)
        else:
            user = self.get_user_by_username(db, cred)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user
    
    def infer_user_login_method(self,db:Session,cred:str)->Users|None:
        if FormHelper.is_valid_email(cred):
            user = self.get_user_by_email(db=db, email=cred)
        else:
            user = self.get_user_by_username(db=db, username=cred)
        return user
    
    def create_access_token(self,data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)
        return encoded_jwt

    def get_current_user(self,token: Annotated[str, Depends(oauth2_scheme)],db:Session=Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.__SECRET_KEY, algorithms=[self.__ALGORITHM])
            cred: str = payload.get("sub")
            if cred is None:
                raise credentials_exception
            token_data = TokenData(cred=cred)
        except JWTError:
            raise credentials_exception      
        user=self.infer_user_login_method(db=db,cred=token_data.cred)
        if user is None:
            raise credentials_exception
        return user

    def create_user(self,db: Session, user: SignUpForm):
        db_user = Users(
            username=user.username,
            email=user.email,
            hashed_password=self.get_password_hash(user.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user







