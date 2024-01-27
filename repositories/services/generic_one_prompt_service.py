from fastapi import HTTPException
from sqlalchemy.orm import Session
from forms.chat_query import ChatQuery
from repositories.vector_repository import VectorRepository
from langchain.chains.summarize import load_summarize_chain
class GenericOnePromptService():
    
    
      
    SUMMARY_QUERY="Write a precise  and concise summary yey informative and usefull of the following text:"
    
    KEY_WORD_QUERY="Get the keywords of the following text:"
    
    def __init__(self,task:str):
        self.task=task

   
    def handle(self,chat_id:int,db:Session,model):
        if self.task not in ["Summarization","Keyword-extraction","Chat"]:
            raise HTTPException(status_code=400,detail= "Invalid task")
        vectordb = VectorRepository.get_vector_store(chat_id,db)
        chain = load_summarize_chain(model, chain_type="stuff")
        search = vectordb.similarity_search(" ")
        answer = chain.run(input_documents=search, question=self.query_selector())
        return answer
       
            
    
    
    
        

    def query_selector(self):
        if self.task=="Summarization":
            return GenericOnePromptService.SUMMARY_QUERY
        elif self.task=="Keyword-extraction":
            return GenericOnePromptService.KEY_WORD_QUERY
        return GenericOnePromptService.SUMMARY_QUERY
        
    
  