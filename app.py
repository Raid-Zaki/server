from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import dotenv
dotenv.load_dotenv()
models={}
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Load the ML model
    #models[Embedders.FLAN_SMALL.value]=HuggingFaceBgeEmbeddings(model_name=Embedders.FLAN_SMALL.value,cache_folder=os.getenv("CACHE_FOLDER"))
    yield
    # Clean up the ML models and release the resources
    models.clear()