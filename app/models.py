from uuid import uuid4, UUID
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Loan Amortization API")

class UserCreate(BaseModel):
    name: str = Field(..., example = "Oscar")

class User(BaseModel):
    id: UUID
    name: str

class LoanCreate(BaseModel):
    amount: float = Field(..., gt=0, example=5000.0)
    annual_interest_rate: float = Field(..., gt=0, example=0.05)
    loan_term_months: int = Field(..., gt=0, example=12)
    user_id: UUID

class Loan(BaseModel):
    id: UUID
    amount: float
    annual_interest_rate: float
    loan_term_months: int
    owner_id: UUID
    shared_with: List[UUID] = []

class LoanScheduleItem(BaseModel):
    month: int
    remaining_balance: float
    monthly_payment: float

class LoanSummary(BaseModel):
    month: int
    current_principal_balance: float
    total_principal_paid: float
    total_interest_paid: float
