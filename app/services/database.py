from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.attendance import Attendance

SQLALCHEMY_DATABASE_URL = "sqlite:///./attendance.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Create the tables for the models
    User.__table__.create(bind=engine, checkfirst=True)
    Attendance.__table__.create(bind=engine, checkfirst=True)
    
def get_db():
    db = SessionLocal()
    try:
        yield db  # This will provide the db session to be used in your routes
    finally:
        db.close() 