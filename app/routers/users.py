# app/routers/users.py

from uuid import uuid4, UUID
from typing import List
from fastapi import APIRouter, HTTPException

from app.models import User, UserCreate, Loan
from app.db import users_db, user_loans_map, loans_db

router = APIRouter()

@router.post("", response_model=User)
def create_user(user_in: UserCreate):
    new_id = uuid4()
    user = User(id=new_id, name=user_in.name)
    users_db[new_id] = user
    user_loans_map[new_id] = set()
    return user

@router.get("/{user_id}", response_model=User)
def get_user(user_id: UUID):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
