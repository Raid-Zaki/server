from datetime import datetime
import uuid
from sqlalchemy import Column, String,TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base, engine
class Posts(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String)
    description = Column(String)
   
    
class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String,nullable=False,unique=True)
    email=Column(String,nullable=False,unique=True)
    hashed_password=Column(String,nullable=False)
    created_at = Column(TIMESTAMP,default=datetime.now())
    updated_at = Column(TIMESTAMP,default=datetime.now())

    
Base.metadata.create_all(bind=engine)