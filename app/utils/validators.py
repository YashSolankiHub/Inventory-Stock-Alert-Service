from passlib.context import CryptContext 
import re

class PwdContext:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

    #convert plain password into hash password and return it
    def get_hash_password(self, plain_password):
        return self.pwd_context.hash(plain_password)
    
    #verify user entered password with stored password
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    


# p1 = PwdContext()
# print(p1.get_hash_password("india@123"))


class Validators:
    #static method for validating mobile number
    @staticmethod
    def validate_mobile(value:int):
        if len(str(value)) != 10:
            raise ValueError("Mobile number must be 10 digit")

        return value
    
    #static method for validating username
    @staticmethod 
    def validate_username(value:str):
        if not re.match(r'^[a-zA-Z0-9_.-]{4,20}$', value):
            raise ValueError("Username must be 4-20 characters and can only contain letters, numbers, _, ., -")
        return value
    

    
    
    
    

    

