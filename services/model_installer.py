import os,sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)   
import dotenv
from fastapi import UploadFile

from services.embedder import Embedder
from utils.enums import Embedders, Splitters


if __name__ == "__main__":
    
    dotenv.load_dotenv()
    
    cache_dir=os.getenv("CACHE_FOLDER")
    models=[Embedders.FLAN_SMALL]
    if not os.path.exists(cache_dir):
        os.chmod(cache_dir,0o777)
        os.rmdir(cache_dir)

    for model in models:
        
        data=UploadFile(file=open("temp/files.txt","rb"))
        embedder=Embedder(media=UploadFile(file=open("temp/files.txt","rb")),embedder_name=model,
                      spliter=Splitters.CHAR)
        
        print(embedder.embedd())