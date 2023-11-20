from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy_utils import database_exists, create_database
import dotenv

dotenv.load_dotenv()
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(os.getenv("DB_USER")
                                                               ,os.getenv("DB_PASSWORD")
                                                               ,os.getenv("DB_HOST")
                                                               ,os.getenv("DB_PORT"),
                                                                os.getenv("DB_NAME"))
if(not database_exists(SQLALCHEMY_DATABASE_URL)):
    create_database(SQLALCHEMY_DATABASE_URL)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
