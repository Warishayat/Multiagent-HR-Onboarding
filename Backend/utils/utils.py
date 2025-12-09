from passlib.context import CryptContext
import jwt
from jose import JWTError
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException,status
from models.employee import TokenData
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
O_auth2schema = OAuth2PasswordBearer(tokenUrl="/user/login")




def hashPassword(password:str):
    return pwd_context.hash(password)

def verifyPassword(plain_password:str,hash_password:str):
    return pwd_context.verify(plain_password,hash_password)

def Create_Acess_token(data:dict):
    to_encode=data.copy()
    EXPIRE = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":EXPIRE})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt


def verifiy_Acess_token(token:str, credential_Exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,[ALGORITHM])
        user_id=payload.get("user_id")
        if not user_id:
            raise credential_Exception
        token_data=TokenData(id=user_id)
        return token_data
    except JWTError:
        raise credential_Exception
    

def get_current_user(token:str=Depends(O_auth2schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldnot validatae credentials",headers={"WWW-Authenticate": "Bearer"})
    return verifiy_Acess_token(token,credential_Exception=credentials_exception)