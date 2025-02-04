# app/routers/users.py

from uuid import uuid4, UUID
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from app.models import User, UserCreate, Loan, LoanShare
from sqlmodel import Session, select
from app.db import get_session
from sqlalchemy import or_


router = APIRouter()

# POST new user
@router.post("", response_model=User)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    user = User(name=user_in.name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user 

# GET all users
@router.get("/all", response_model=List[User], summary="Fetch all users")
def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

# GET user by id
@router.get("/{user_id}", response_model=User)
def get_user(user_id: UUID, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# GET all loans for a user
@router.get("/{user_id}/loans", summary="Fetch all loans for a user")
def get_loans_for_user(user_id: UUID, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    owned_loans = session.exec(select(Loan).where(Loan.owner_id == user_id)).all()
    shared_loan_ids = session.exec(select(LoanShare.loan_id).where(LoanShare.user_id == user_id)).all()
    shared_loan_ids = [loan_id for loan_id in shared_loan_ids]
    shared_loans = session.exec(select(Loan).where(Loan.id.in_(shared_loan_ids))).all() if shared_loan_ids else []
    return owned_loans + shared_loans
