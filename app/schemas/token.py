from pydantic import BaseModel

class Token(BaseModel):
    username:str
    access_token :str
    refresh_token : str
    token_type: str

    