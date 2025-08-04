from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL


#create database engine using databse url
engine = create_engine(DATABASE_URL)


#make session variable which is used to interact with the db
SessionLocal = sessionmaker(bind=engine)



#yield 
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db = SessionLocal()


