
from enum import Enum

class Splitters(Enum):
    SENTENCE = "sentence"
    RECURSIVE = "recursive"
    CHAR ="character" 
    
class Embedders(Enum):
    
    FLAN_SMALL= "google/flan-t5-small"
