import re
class FormHelper:
    
    @staticmethod 
    def is_valid_email(cred:str)->bool:
        return True if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', cred) else False