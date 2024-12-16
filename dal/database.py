from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/db_name"


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """
    Initialize the database by creating all tables.
    """
    import models  # Import models here to register with the Base
    Base.metadata.create_all(bind=engine)

def get_session():
    """
    Provide a session for database transactions.
    """
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()