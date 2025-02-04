from uuid import uuid4, UUID
from typing import Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import JSON, String
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.ext.mutable import MutableList


app = FastAPI(title="Loan Amortization API")

def uuid_serializer(obj):
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


class UserCreate(BaseModel):
    name: str = Field(..., description= "Oscar")

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str

class LoanCreate(BaseModel):
    amount: float = Field(..., gt=0, description=5000.0)
    annual_interest_rate: float = Field(..., gt=0, description=0.05)
    loan_term_months: int = Field(..., gt=0, description=12)
    owner_id: UUID

class Loan(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    amount: float
    annual_interest_rate: float
    loan_term_months: int
    owner_id: UUID  
    shared_with: Optional[List[str]] = Field(default_factory=list, sa_column=Column(MutableList.as_mutable(JSON)))


class LoanScheduleItem(BaseModel):
    month: int
    remaining_balance: float
    monthly_payment: float

class LoanSummary(BaseModel):
    month: int
    current_principal_balance: float
    total_principal_paid: float
    total_interest_paid: float

class LoanShareRequest(BaseModel):
    other_user_id: UUID
