from sqlalchemy.orm import Session
from repositories.vector_repository import VectorRepository
from langchain.chains.summarize import load_summarize_chain

class SummaryService():
    @staticmethod 
    def summarize(chat_id:int,db:Session,model):
        vectordb = VectorRepository.get_vector_store(chat_id,db)
        chain = load_summarize_chain(model, chain_type="stuff")
        search = vectordb.similarity_search(" ")
        summary = chain.run(input_documents=search, question="Write a summary within 150 words.")
        return summary
        
  