# test_db.py
from db import init_db, get_test_session
from models import User, Loan
from sqlmodel import Session, select

# Initialize database
init_db()

# Test adding a user
def test_user_creation():
    session = get_test_session()
    try:
        user = User(name="Test User")
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"Created User: {user.id} - {user.name}")
    finally:
        session.close() 

# Test adding a loan
def test_loan_creation():
    session = get_test_session()
    try:
        user = session.exec(select(User)).first()
        if not user:
            print("No users found. Please run test_user_creation() first.")
            return
        
        loan = Loan(
            amount=1000.0,
            annual_interest_rate=0.05,
            loan_term_months=12,
            owner_id=user.id
        )
        session.add(loan)
        session.commit()
        session.refresh(loan)
        print(f"Created Loan: {loan.id} for User {loan.owner_id}")
    finally:
        session.close()
    
# Run Tests
if __name__ == "__main__":
    test_user_creation()
    test_loan_creation()
