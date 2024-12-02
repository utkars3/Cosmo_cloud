#pydantic is used for data validation
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Address(BaseModel):
    city:str
    country:str

class Student(BaseModel):     #inherit basemodel
    name:str
    age:int
    address:Address

class StudentCreateResponse(BaseModel):
    id:str    
    
class UpdateStudentRequest(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[dict] = None