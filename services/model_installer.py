from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
import os 
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.enums import Embedders

def download_models(model_names):
    for model_name in model_names:
        # Create a new model instance
        model = HuggingFaceEndpoint(model_name=model_name,)
        # Download the model
        model.download()
        
print(download_models([Embedders.FLAN_SMALL]))