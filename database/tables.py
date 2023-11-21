import uuid
from sqlalchemy import Column, String
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
    full_name=Column(String,nullable=False)
    hashed_password=Column(String,nullable=False)
Base.metadata.create_all(bind=engine)