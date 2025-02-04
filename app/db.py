# app/db.py

from sqlmodel import SQLModel, Session, create_engine
from app.models import User, Loan, LoanShare

DATABASE_URL = "sqlite:///database.db"  

engine = create_engine(DATABASE_URL, echo=True)
def init_db():
    print("Initializing database")
    SQLModel.metadata.create_all(engine)

# Dependency to get a session for requests
def get_session():
    with Session(engine) as session:
        yield session

def get_test_session():
    return Session(bind=engine)
