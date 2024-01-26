from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import  RunnablePassthrough
from langchain.llms.huggingface_hub import HuggingFaceHub
from database.tables import Chats, Messages
from forms.chat_query import ChatQuery
from models.message import Message
from repositories.vector_repository import VectorRepository
from sqlalchemy.orm import Session
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory,ConversationBufferMemory


import dotenv
import os 

dotenv.load_dotenv()

class ChatRepository:
    
    
    @staticmethod
    async def resolve_chat_query(query:ChatQuery,id:int,db:Session)->Message:
        chat=db.query(Chats).filter(Chats.id==id).first()
        messages=chat.messages
        if len(chat.messages)==0:
            return await ChatRepository.__chat_creation_template(query,id,db)
        else:
            return await ChatRepository.__chat_history_template(query,id,db,messages)



    @staticmethod 
    async def __chat_creation_template(query:ChatQuery,id:int,db:Session)->Message:
        model = ChatRepository.__get_chat_model()
        retriever =await  VectorRepository.query(query.query, id, db)
        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = (
                {"context": retriever ,"question": RunnablePassthrough()}
                | prompt
                | model
                | StrOutputParser()
        )
        response=chain.invoke(query.query)
        message=ChatRepository.__create_message(response,query.query,id,db)
        return message
        
    @staticmethod 
    async def __chat_history_template(query:ChatQuery,id:int,db:Session,messages:list[Messages])->Message:
        history=ChatRepository.__prepare_history(messages)
        retriever =await  VectorRepository.query(query.query, id, db)
        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=history,return_messages=True,output_key='answer')
        template = """Given the following conversation history and the context given , do your best to answer the human question:
        Useful Informations:
        {context}
        
        Chat History:{chat_history}
        
        Current Question: {question}
        """
        PROMPT = PromptTemplate(
            input_variables=["chat_history", "question"], 
            template=template
        )
        model=ChatRepository.__get_chat_model()
        qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT}
        )
        result = qa.invoke(query.query)
        message=ChatRepository.__create_message(result['answer'],query.query,id,db)
        return message
    
    
    @staticmethod 
    def __prepare_history(messages:list[Messages]):
        history=ChatMessageHistory()
        for message in messages:
            history.add_user_message(message.human_question)
            history.add_ai_message(message.bot_answer)

        return history
        
        
    @staticmethod 
    def __get_chat_model():
        model = HuggingFaceHub(
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        task="text-generation",
        model_kwargs={
            "max_new_tokens": 250,
            "top_k": 30,
            "temperature": 0.1,
            "repetition_penalty": 1.03,
        },
        )
        return model
    
    @staticmethod 
    def __create_message(answer:str,question:str,chat_id:int,db:Session)->Message:
        chat_message=Messages(human_question=question,bot_answer=answer,chat_id=chat_id)
        db.add(chat_message)
        db.commit()
        db.refresh(chat_message) 
        return Message.model_validate(chat_message) 
        

      




        