from uuid import uuid4, UUID
from typing import List
from fastapi import APIRouter, HTTPException, Query

from app.models import (
    LoanCreate, Loan, LoanScheduleItem, LoanSummary
)
from app.db import loans_db, users_db, user_loans_map
from app.calculation.amortization import (
    generate_amortization_schedule,
    get_loan_summary_for_month
)

router = APIRouter()

# POST a new loan
@router.post("", response_model=Loan, summary="Add a new loan")
def create_loan(loan_in: LoanCreate):
    if loan_in.owner_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    if loan_in.amount <= 0:
        raise HTTPException(status_code=422, detail="Loan Amount most be positive")
        
    new_id = uuid4()
    loan = Loan(id=new_id, 
                amount=loan_in.amount, 
                annual_interest_rate=loan_in.annual_interest_rate, 
                loan_term_months=loan_in.loan_term_months,
                owner_id=loan_in.owner_id)
    loans_db[new_id] = loan
    user_loans_map[loan.owner_id].add(loan.id)
    return loan
# GET an existing loan
@router.get("/{loan_id}", response_model=Loan, summary="Fetch an existing loan")
def get_loan(loan_id: UUID):
    loan = loans_db.get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
# GET all existing loans
@router.get("/", response_model=List[Loan], summary="Fetch all existing loans")
def get_all_loans():
    return list(loans_db.values())

# GET loan amortization schedule
@router.get("/{loan_id}/schedule", response_model=List[LoanScheduleItem], summary="Fetch remaining loan schedule")
def get_loan_schedule(loan_id: UUID):
    loan = loans_db[loan_id]
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return generate_amortization_schedule(loan)

# GET monthly payment summary
@router.get("/{loan_id}/summary", response_model=LoanSummary, summary="Fetch summary of monthly payment")
def get_loan_summary(loan_id: UUID, month: int = Query(..., gt=0, lt=13)):
    loan = loans_db.get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return get_loan_summary_for_month(loan, month)

