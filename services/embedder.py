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
class Embedder:
   
    
    COLLECTION_NAME="media_embeddings"
    def __init__(self,media:UploadFile,spliter:Splitters=Splitters.SENTENCE,embedder:Embedders=Embedders.FLAN_SMALL):
        self.media = media
        self.model_name=embedder.value
        self.document_splitter = self.splitter_factory(spliter)
        self.embedder = HuggingFaceBgeEmbeddings(model_name=embedder.value)
    def __await__(self):
        return self.create().__await__()
    async def create(self):
        self.document_loader=await self.loader_factory()
        return self
    async def loader_factory(self):

        if self.media.content_type == "application/pdf":
            path=await self.save_file(".pdf")
            file_loader=PyPDFLoader(file_path=path)
        else :
            path=await self.save_file(".txt")
            file_loader= TextLoader(path)
        
        os.remove(path=path)
        return file_loader
    
    
    def splitter_factory(self,spliter:Splitters):
        if spliter == Splitters.SENTENCE:
            return SentenceTransformersTokenTextSplitter(model_name=self.model_name)
        elif spliter == Splitters.RECURSIVE:
            return RecursiveCharacterTextSplitter()
        elif spliter == Splitters.CHAR:
            return CharacterTextSplitter()
        else:
            return TokenTextSplitter()
    
    
    def embedd(self):
        documents = self.document_loader.load_and_split()
        documents = self.document_splitter.split(documents)
        dotenv.load_dotenv()
        db = PGVector.from_documents(embedding=self.embedder, documents=documents, connection_string=DATABASE_URL, collection_name=Embedder.COLLECTION_NAME)
        db.insert()
        return db
    def pipeline(self,query:str):
        documents = self.document_loader.load_and_split()
        documents = self.document_splitter.split(documents)
        dotenv.load_dotenv()
        db = PGVector.from_documents(embedding=self.embedder, documents=documents, connection_string=DATABASE_URL, collection_name=Embedder.COLLECTION_NAME)
        return db.similarity_search_with_score(query=query,k=5)
    
    async def save_file(self,file_type)->str:
        path="/temp/{}".format(str(uuid.uuid4())+file_type)
        with open(path,"wb") as f:
            f.write(await self.media.file.read())
        return path
       
            
        
            
            
        



