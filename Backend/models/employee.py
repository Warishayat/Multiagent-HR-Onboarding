from pydantic import BaseModel,EmailStr
from typing import Optional
import datetime


class EmployeeValidation(BaseModel):
    id : int 
    name: str
    email: EmailStr
    role: str
    start_date : datetime.date
    status : str

class ValidateSignup(BaseModel):
    name:str
    email:EmailStr
    password:str

class SignupResponse(BaseModel):
    id:int
    name:str
    email:EmailStr

    class Config:
        from_attributes = True

class ValidateLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id : Optional[int] = None

class TokenData(BaseModel):
    id : Optional[int] = None