from datetime import datetime
import uuid
from sqlalchemy import  JSON, Column, String,TIMESTAMP,Integer
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base,Mapped
from database.connection import Base, engine
from typing import List
from pgvector.sqlalchemy import Vector



Base = declarative_base()
class Posts(Base):
    __tablename__ = "posts"
    id= Column(Integer,primary_key=True)
    title = Column(String)
    description = Column(String)
   

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer ,primary_key=True)
    username = Column(String,nullable=False,unique=True)
    email=Column(String,nullable=False,unique=True)
    hashed_password=Column(String,nullable=False)
    created_at = Column(TIMESTAMP,default=datetime.now())
    updated_at = Column(TIMESTAMP,default=datetime.now())
    
    
    medias:Mapped[List["Medias"]] = relationship("Medias",)
    chats:Mapped[List["Chats"]] = relationship("Chats",secondary="medias",overlaps="medias")
    collections:Mapped[List["PgCollections"]] = relationship("PgCollections",secondary="user_collections",overlaps="collections")
  

    
    
class MediaTypes(Base):
    __tablename__ = "media_types"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    
    medias:Mapped[List["Medias"]] = relationship("Medias")
    chats:Mapped[List["Chats"]] = relationship("Chats",secondary="medias",overlaps="medias,chats")
    
class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    
    chats:Mapped[List["Chats"]] = relationship("Chats")
    
class Medias(Base):
    "table name"
    __tablename__ = "medias"
    "ids"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    media_type_id = Column(Integer,ForeignKey("media_types.id"))
    
    " fields"
    title=Column(String,nullable=False)
    "time stamps"
    created_at = Column(TIMESTAMP,default=datetime.now())
    updated_at = Column(TIMESTAMP,default=datetime.now())
    "relationships"
    user:Mapped["Users"] = relationship("Users",overlaps="chats,medias")
    chats:Mapped[List["Chats"]] = relationship("Chats",overlaps="chats,chats")
    mediaType:Mapped["MediaTypes"]=relationship("MediaTypes",overlaps="chats,medias")
    
    embeddings:Mapped[List["PgEmbeddings"]] = relationship("PgEmbeddings")
    
    

class PgCollections(Base):
    __tablename__ = "langchain_pg_collection"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name=Column(String,nullable=False)
    cmetadata=Column(JSON,nullable=True)
    embeddings:Mapped[List["PgEmbeddings"]] = relationship("PgEmbeddings")
    

class UserCollections(Base):
    
    __tablename__ = "user_collections"
   
    user_id = Column(Integer,ForeignKey("users.id"),primary_key=True)
    pg_collection_id = Column(UUID(as_uuid=True),ForeignKey("langchain_pg_collection.uuid"),primary_key=True)
    created_at = Column(TIMESTAMP,default=datetime.now())
    updated_at = Column(TIMESTAMP,default=datetime.now())
    
    pgCollection:Mapped["PgCollections"] = relationship("PgCollections",overlaps="collections" )
    user:Mapped["Users"] = relationship("Users",overlaps="collections,userCollections")

    
    
class PgEmbeddings(Base):
    
    __tablename__ = "langchain_pg_embedding"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    collection_id = Column(UUID(as_uuid=True),ForeignKey("langchain_pg_collection.uuid"))
    embedding=Column(Vector,nullable=False)
    document=Column(String,nullable=False)
    cmetadata=Column(JSON,nullable=True)
    #"custom_id" is a custom id will be used for the media_id
    custom_id= Column(UUID(as_uuid=True),ForeignKey("medias.id"))
    collection:Mapped["PgCollections"] = relationship("PgCollections",overlaps="embeddings")
    media:Mapped["Medias"] = relationship("Medias",overlaps="embeddings")


class Chats(Base):
    __tablename__ = "chats"
    id= Column(Integer, primary_key=True)
    media_id = Column(ForeignKey("medias.id"))
    task_id = Column(ForeignKey("tasks.id"))
    
    created_at = Column(TIMESTAMP,default=datetime.now())
    updated_at = Column(TIMESTAMP,default=datetime.now())
    
    media:Mapped["Medias"]=relationship("Medias",overlaps="chats,chats,chats")
    user:Mapped["Users"]=relationship("Users",secondary="medias",overlaps="chats,media,chats,user,medias")
    messages:Mapped[List["Messages"]] =relationship("Messages")
    taks:Mapped["Tasks"]=relationship("Tasks",overlaps="chats")
    
class Messages(Base):
    __tablename__ = "messages"
    id= Column(Integer, primary_key=True)
    chat_id = Column(ForeignKey("chats.id"))

    human_question = Column(String,nullable=False)
    bot_answer = Column(String,nullable=True)
    created_at = Column(TIMESTAMP,default=datetime.now())
    updated_at = Column(TIMESTAMP,default=datetime.now())
    
    chat:Mapped["Chats"] =relationship("Chats",overlaps="messages,chats,chats,chats")
    media:Mapped["Medias"] =relationship("Medias",secondary="chats",overlaps="chat,messages,media,user,chats,chats,chats")

    
Base.metadata.create_all(bind=engine)