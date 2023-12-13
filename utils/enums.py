
from enum import Enum

class Splitters(Enum):
    SENTENCE = "sentence"
    RECURSIVE = "recursive"
    CHAR ="character" 
    
class Embedders(Enum):
    
    HF = "huggingface"
