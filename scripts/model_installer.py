import os,sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)   
from langchain.embeddings import HuggingFaceBgeEmbeddings
import dotenv
from utils.enums import Embedders


if __name__ == "__main__":
    
    dotenv.load_dotenv()
    
    cache_dir=os.getenv("CACHE_FOLDER")
    models=[Embedders.FLAN_SMALL]
    if os.path.exists(cache_dir):
        # os.chmod(cache_dir,0o777)
        os.rmdir(cache_dir)

    for model in models:
        model=HuggingFaceBgeEmbeddings(model_name=model.value,cache_folder=cache_dir)
      
        
