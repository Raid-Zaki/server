from datetime import datetime
from sqlalchemy import Column, String,TIMESTAMP,Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, declarative_base,Mapped
from database.connection import Base, engine
from typing import List



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
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    media_type_id = Column(Integer,ForeignKey("media_types.id"))
    
    " fields"
    content = Column(String,nullable=False)
    title=Column(String,nullable=False)
    "time stamps"
    created_at = Column(TIMESTAMP,default=datetime.now())
    updated_at = Column(TIMESTAMP,default=datetime.now())
    "relationships"
    user:Mapped["Users"] = relationship("Users",overlaps="chats,medias")
    chats:Mapped[List["Chats"]] = relationship("Chats",overlaps="chats,chats")
    mediaType:Mapped["MediaTypes"]=relationship("MediaTypes",overlaps="chats,medias")
    
    


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
    # user:Mapped["Users"] =relationship("Users",secondary="medias")


Base.metadata.create_all(bind=engine)