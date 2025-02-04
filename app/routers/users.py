# app/routers/users.py

from uuid import uuid4, UUID
from typing import List
from fastapi import APIRouter, HTTPException

from app.models import User, UserCreate, Loan
from app.db import users_db, user_loans_map, loans_db

router = APIRouter()

# POST new user
@router.post("", response_model=User, summary="Add a new user")
def create_user(user_in: UserCreate):
    new_id = uuid4()
    user = User(id=new_id, name=user_in.name)
    users_db[new_id] = user
    user_loans_map[new_id] = set()
    return user

# GET user by id
@router.get("/{user_id}", response_model=User, summary="Fetch a user")
def get_user(user_id: UUID):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# GET all users
@router.get("/", response_model=List[User], summary="Fetch all users")
def get_all_users():
    return list(users_db.values())

@router.get("/{user_id}/loans", response_model=List[Loan])
def get_all_loans_for_user(user_id: UUID):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    loan_ids = user_loans_map[user_id]
    results = []
    for lid in loan_ids:
        loan = loans_db.get(lid)
        if loan:
            results.append(loan)
    return results

