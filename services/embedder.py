from fastapi import UploadFile
from langchain.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import SentenceTransformersTokenTextSplitter,RecursiveCharacterTextSplitter,CharacterTextSplitter,TokenTextSplitter
from langchain.embeddings import HuggingFaceBgeEmbeddings
from database.connection import DATABASE_URL
from utils.enums import Embedders, Splitters
from langchain.vectorstores.pgvector import PGVector
import uuid 
import os
import dotenv
dotenv.load_dotenv()
from app import models
class Embedder:
   
    COLLECTION_NAME="media_embeddings"
    CACHE_FOLDER=os.getenv("CACHE_FOLDER")
    def __init__(self,media:UploadFile,spliter:Splitters=Splitters.RECURSIVE,embedder_name:Embedders=Embedders.FLAN_SMALL):
        self.media = media
        self.model_name=embedder_name.value
        self.document_splitter = self.splitter_factory(spliter)
        self.embedder = models[embedder_name.value]
    def loader_factory(self):
        if self.media.content_type == "application/pdf":
            path= self.save_file(".pdf")
            file_loader=PyPDFLoader(file_path=path)
        else :
            path= self.save_file(".txt")
            file_loader= TextLoader(path)
        
        #os.remove(path=path)
        return file_loader
    
    def splitter_factory(self,spliter:Splitters):
        if spliter == Splitters.SENTENCE:
            return SentenceTransformersTokenTextSplitter(
                tokens_per_chunk=10,
                model_name=self.model_name)
        elif spliter == Splitters.RECURSIVE:
            return RecursiveCharacterTextSplitter()
        elif spliter == Splitters.CHAR:
            return CharacterTextSplitter()
        else:
            return TokenTextSplitter()
    
    def embedd(self):
        document_loader =  self.loader_factory()
        documents = document_loader.load_and_split(self.document_splitter)
        db = PGVector.from_documents(embedding=self.embedder, documents=documents, connection_string=DATABASE_URL, collection_name=Embedder.COLLECTION_NAME)
        return db
    
    def pipeline(self,query:str):
        document_loader=self.loader_factory()
        documents = document_loader.load_and_split(text_splitter=self.document_splitter)      
        db = PGVector.from_documents(embedding=self.embedder, documents=documents, connection_string=DATABASE_URL, collection_name=Embedder.COLLECTION_NAME)
        return db.similarity_search_with_score(query=query,k=5)

    def save_file(self,file_type)->str:
        path="temp/{}".format(str(uuid.uuid4())+file_type)
        with open(path,"wb") as f:
            f.write(self.media.file.read())
        return path
       
            
        
            
            

   


