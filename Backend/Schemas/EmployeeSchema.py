from sqlalchemy import Column,Integer,String,Boolean,DateTime,Date
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from Database.database import Base


class Employeesdata(Base):
    __tablename__ = "Employee"
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email  = Column(String,unique=True,nullable=False)
    role = Column(String,nullable=False)
    start_date = Column(Date,nullable=False)
    status = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class UserCredentialsData(Base):
    __tablename__ = "UserCredential"
    id =  Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=True)
    email = Column(String,nullable=True)
    password = Column(String,nullable=True)
    created_At = Column(TIMESTAMP(timezone=True),nullable=True,server_default=(text("now()")))