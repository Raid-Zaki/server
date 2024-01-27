from fastapi import UploadFile
from langchain.document_loaders import TextLoader,PyPDFLoader
from langchain.text_splitter import SentenceTransformersTokenTextSplitter,RecursiveCharacterTextSplitter,CharacterTextSplitter,TokenTextSplitter
from database.connection import DATABASE_URL
from database.tables import Chats, Medias
from forms.chat_query import ChatQuery
from forms.upload_form import UploadForm

from models.user import User
from repositories.media_repository import MediaRepository
from utils.enums import  Splitters
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings

from sqlalchemy.orm import Session
import uuid 
import os
import dotenv
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document

from utils.model_selector import ModelSelector
dotenv.load_dotenv()
class VectorRepository:
   
    
    __api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    def __init__(self,media:UploadFile,user:User, spliter:Splitters=Splitters.RECURSIVE):
        self.__media = media
        self.user=user
        self.__model_name=ModelSelector().select_model()
        (self.__loader,self.path)=self.__loader_factory()
        self.__document_splitter = self.__splitter_factory(spliter)
        self.__embedder = HuggingFaceInferenceAPIEmbeddings(model=self.__model_name,api_key=VectorRepository.__api_key)
        
    async def embedd(self,db:Session,data:UploadForm)->Medias:
      
        media=MediaRepository.create(data=data,user=self.user,db=db)
        vector_db=PGVector(connection_string=DATABASE_URL,embedding_function=self.__embedder,collection_name=str(media.id))
      
        documents = self.__loader.load_and_split(self.__document_splitter)
        VectorRepository.clean_docs(documents)
        await vector_db.aadd_documents(documents,ids=[media.id for i in range(len(documents))])
        return media
    
    
    async def get_retreiver(query:ChatQuery,id:int,db:Session)->VectorStoreRetriever:
        
        # a function to infer the model used based on the user task
        chat=db.query(Chats).filter(Chats.id==id).first()
        embedder=HuggingFaceInferenceAPIEmbeddings(model=ModelSelector().select_model(chat.task),api_key=VectorRepository.__api_key)
        db=PGVector(connection_string=DATABASE_URL,embedding_function=embedder,collection_name=str(chat.media_id))
        return db.as_retriever()
    
    
    def get_vector_store(id:int,db:Session):
        chat=db.query(Chats).filter(Chats.id==id).first()
        embedder=HuggingFaceInferenceAPIEmbeddings(model=ModelSelector().select_model(chat.task),api_key= VectorRepository.__api_key)
        vector_store=PGVector(connection_string=DATABASE_URL,embedding_function=embedder,collection_name=str(chat.media_id))
        return vector_store
    

    async def delete_temp_file(self):
        os.remove(self.path)
        
        
    def __loader_factory(self):
        if self.__media.content_type == "application/pdf":
            path= self.__save_file(".pdf")
            file_loader=PyPDFLoader(file_path=path,extract_images=True)
        else :
            path= self.__save_file(".txt")
            file_loader= TextLoader(file_path=path)
    
        return (file_loader,path)
    
    
    @staticmethod
    def  save_and_get_doc_loader(file:UploadFile)->TextLoader|PyPDFLoader:
        if file.content_type == "application/pdf":
            path= VectorRepository.save_file(file,".pdf")
            file_loader=PyPDFLoader(file_path=path,extract_images=True)
        else :
            
            path= VectorRepository.save_file(".txt")
            file_loader= TextLoader(file_path=path)
        return file_loader
    
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
       
    @staticmethod 
    def save_file(file:UploadFile,file_type:str)->str:
        
        path="temp/{}".format(str(uuid.uuid4())+file_type)
        with open(path,"wb") as f:
            f.write(file.read())
        return path
    
    
    @staticmethod
    
    def clean_docs(docs:list[Document]):
        for doc in docs:
            doc.page_content=doc.page_content.replace('\x00', '')
        
       
        
            
            

   


