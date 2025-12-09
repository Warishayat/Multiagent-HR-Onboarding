from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Database_uri = os.getenv('DATABASE_URI')
engine = create_engine(connect_args=Database_uri)
SessionLocal =  sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base =  declarative_base()




def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()