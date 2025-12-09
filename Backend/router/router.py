from fastapi import APIRouter,HTTPException,Depends,status
from models.employee import EmployeeValidation,SignupResponse,ValidateSignup,ValidateLogin
from Database.database import get_db_connection
from Schemas.EmployeeSchema import Employeesdata,UserCredentialsData
from utils.utils import hashPassword,verifyPassword,Create_Acess_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/user",
    tags=["Login/Signup","Employees"]
)


@router.post("/registerUser",response_model=SignupResponse)
async def RegisterUser(data:ValidateSignup,db:Session = Depends(get_db_connection)):
    ExistUser = db.query(UserCredentialsData).filter(UserCredentialsData.email == data.email).first()
    if ExistUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User already Exist"
        )
    hashpass = hashPassword(password=data.password)
    newUser = UserCredentialsData(
        name = data.name,
        email = data.email,
        password = hashpass
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return {
        status:200,
        "name" : data.name,
        "email" : data.email
    }


@router.post("/login")
async def LoginHandle(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db_connection)):
    existingUser = db.query(UserCredentialsData).filter(UserCredentialsData.email == form_data.username).first()
    if not existingUser:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Credential are invalid" 
        )
    verify_hahsed = verifyPassword(form_data.password,existingUser.password)
    if not verify_hahsed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Invalid Credetials"
        )
    access_token = Create_Acess_token(data={"user_id":existingUser.id})
    return {
        "acess_token" : access_token,
        "token_type" : "Bearer"
    }
    