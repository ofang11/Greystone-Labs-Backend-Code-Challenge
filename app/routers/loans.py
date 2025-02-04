from uuid import uuid4, UUID
from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from app.db import get_session
from app.models import (LoanCreate, Loan, LoanScheduleItem, LoanSummary, LoanShareRequest, User)
from sqlmodel import Session, select
import json
from app.calculation.amortization import (generate_amortization_schedule, get_loan_summary_for_month)



router = APIRouter()

# POST a new loan
@router.post("", status_code=201, response_model=Loan)
def create_loan(loan_in: LoanCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == loan_in.owner_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if loan_in.amount <= 0:
        raise HTTPException(status_code=400, detail="Loan amount must be greater than zero")

    if loan_in.annual_interest_rate < 0:
        raise HTTPException(status_code=400, detail="Annual interest rate cannot be negative")

    loan = Loan(**loan_in.model_dump())
    session.add(loan)
    session.commit()
    session.refresh(loan)
    return loan

# GET all existing loans
@router.get("/all", response_model=List[Loan], summary="Fetch all loans")
def get_all_loans(session: Session = Depends(get_session)):
    loans = session.exec(select(Loan)).all()
    return loans

# GET an existing loan
@router.get("/{loan_id}", response_model=Loan)
def get_loan(loan_id: UUID, session: Session = Depends(get_session)):
    loan = session.exec(select(Loan).where(Loan.id == loan_id)).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

# GET loan amortization schedule
@router.get("/{loan_id}/schedule", response_model=list[LoanScheduleItem], summary="Fetch loan schedule")
def get_loan_schedule(loan_id: UUID, session: Session = Depends(get_session)):
    loan = session.exec(select(Loan).where(Loan.id == loan_id)).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    schedule = generate_amortization_schedule(loan)
    return schedule

# GET monthly payment summary
@router.get("/{loan_id}/summary", response_model=LoanSummary, summary="Fetch loan summary for a specific month")
def get_loan_summary(loan_id: UUID, month: int = Query(..., gt=0, lt=13), session: Session = Depends(get_session)):
    loan = session.exec(select(Loan).where(Loan.id == loan_id)).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if month > loan.loan_term_months:
        raise HTTPException(status_code=400, detail="Month out of range")

    return get_loan_summary_for_month(loan, month)

# POST a share loan
@router.post("/{loan_id}/share", summary="Share a loan with another user")
def share_loan(loan_id: UUID, request: LoanShareRequest, session: Session = Depends(get_session)):
    loan = session.exec(select(Loan).where(Loan.id == loan_id)).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    other_user = session.exec(select(User).where(User.id == request.other_user_id)).first()
    if not other_user:
        raise HTTPException(status_code=404, detail="User to share with not found")

    if str(request.other_user_id) not in loan.shared_with:
        loan.shared_with.append(str(request.other_user_id))
        session.add(loan)
        session.commit()
        session.refresh(loan)

    return {"status": "success", "shared_with": loan.shared_with}
