from fastapi import UploadFile
from langchain.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import SentenceTransformersTokenTextSplitter,RecursiveCharacterTextSplitter,CharacterTextSplitter,TokenTextSplitter
from database.connection import DATABASE_URL
from models.medias import UploadForm, UserQuery
from models.users import User
from repositories.media_repository import MediaRepository
from utils.enums import Embedders, Splitters
from langchain.vectorstores.pgvector import PGVector
from sqlalchemy.orm import Session
import uuid 
import os
import dotenv
dotenv.load_dotenv()
from app import models
class VectorRepository:
   
    
    def __init__(self,media:UploadFile,user:User, spliter:Splitters=Splitters.RECURSIVE,embedder_name:Embedders=Embedders.FLAN_SMALL):
        self.__media = media
        self.user=user
        self.__model_name=embedder_name.value
        (self.__loader,self.path)=self.__loader_factory()
        self.__document_splitter = self.__splitter_factory(spliter)
        self.__embedder = models[embedder_name.value]
        
    async def  embedd(self,db:Session,data:UploadForm):
        media=MediaRepository.create(data=data,user=self.user,db=db)
        vector_db=PGVector(connection_string=DATABASE_URL,embedding_function=self.__embedder,collection_name=str(media.id))
        documents = self.__loader.load_and_split(self.__document_splitter)
        await vector_db.aadd_documents(documents,ids=[media.id])
        return True
    
    
    async def query(query:UserQuery,user:User,db:Session):
        
        # a function to infer the model used based on the user task

        
        db=PGVector(connection_string=DATABASE_URL,embedding_function=models[Embedders.FLAN_SMALL.value],collection_name=query.media_id)
        return await db.asimilarity_search_with_score(query=query.query,k=5)
    async def delete_temp_file(self):
        os.remove(self.path)
        

        
        
        
    def __loader_factory(self):
        if self.__media.content_type == "application/pdf":
            path= self.__save_file(".pdf")
            file_loader=PyPDFLoader(file_path=path)
        else :
            path= self.__save_file(".txt")
            file_loader= TextLoader(file_path=path)
        return (file_loader,path)
    
    def __splitter_factory(self,spliter:Splitters):
        if spliter == Splitters.SENTENCE:
            return SentenceTransformersTokenTextSplitter(
                tokens_per_chunk=10,
                model_name=self.__model_name)
        elif spliter == Splitters.RECURSIVE:
            return RecursiveCharacterTextSplitter()
        elif spliter == Splitters.CHAR:
            return CharacterTextSplitter()
        else:
            return TokenTextSplitter()
    

    def __save_file(self,file_type)->str:
        path="temp/{}".format(str(uuid.uuid4())+file_type)
        with open(path,"wb") as f:
            f.write(self.__media.file.read())
        return path
       
            
        
            
            

   


