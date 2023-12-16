# from langchain.document_loaders import PyPDFLoader,TextLoader
# from langchain.text_splitter import SentenceTransformersTokenTextSplitter,RecursiveCharacterTextSplitter,CharacterTextSplitter,TokenTextSplitter
# from langchain.embeddings import HuggingFaceBgeEmbeddings
# from utils.enums import Embedders, Splitters
# from langchain.vectorstores.pgvector import PGVector
# import os
# import dotenv
# class Embedder:
#     MODEL_NAME="google/flan-t5-small"
#     embedder= HuggingFaceBgeEmbeddings(model_name=MODEL_NAME)
#     def __init__(self,media_path:str,spliter:Splitters=Splitters.SENTENCE,embedder:Embedders=Embedders.HF):
#         self.media_path = media_path
#         self.document_loader = self.loader_factory(media_path)
#         self.document_splitter = self.splitter_factory(spliter)
        

#     def loader_factory(self,media_path:str):
#         if media_path.endswith('.pdf'):
#             return PyPDFLoader(media_path)
#         else :
#             return TextLoader(media_path)
#     def splitter_factory(self,spliter:Splitters):
#         if spliter == Splitters.SENTENCE:
#             return SentenceTransformersTokenTextSplitter(model_name=self.MODEL_NAME)
#         elif spliter == Splitters.RECURSIVE:
#             return RecursiveCharacterTextSplitter()
#         elif spliter == Splitters.CHAR:
#             return CharacterTextSplitter()
#         else:
#             return TokenTextSplitter()
        
#     def pipeline(self,query:str):
#         documents = self.document_loader.load_and_split()
#         documents = self.document_splitter.split(documents)
#         dotenv.load_dotenv()
#         db = PGVector.from_documents(embedding=Embedder.embedder, documents=documents, connection_string=os.getenv("DB_CONNECTION_STRING"), collection_name="media_embeddings")
#         return db.similarity_search_with_score(query=query,k=5)
        

            
        
            
            
        



