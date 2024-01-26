from database.tables import Tasks

from models.task import Task
class ModelSelector():
    
    
    def __init__(self):
        pass 
    
    def select_model(self,task:Tasks|Task=None)->str:
        if isinstance(task, Tasks) or isinstance(task, Task):
            task=task.name
        if task=="Summarization":
            return "facebook/bart-large-cnn"
        
        elif task=="Translation":
            return "Unbabel/TowerBase-7B-v0.1"
        elif task=="Chat":
            return "mistralai/Mixtral-8x7B-Instruct-v0.1"
        
        return "mistralai/Mixtral-8x7B-Instruct-v0.1"
    
    
    def to_hg_task(self,task:Tasks|Task=None)->str:
        if isinstance(task, Tasks) or isinstance(task, Task):
            task=task.name
        if task=="Summarization":
            return "summarization"
        
        elif task=="translation":
            return "translation"
        
        
        elif task=="Chat":
            return "text-generation"
        return "text-generation"
    

            
        
            
            