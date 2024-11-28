from pydantic import BaseModel
from typing import Literal
from datetime import date

class User(BaseModel):
    name: str
    username: str
    password: str
    email: str
    gender: Literal['Male', 'Female']
    
   