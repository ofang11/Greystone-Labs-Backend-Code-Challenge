# app/routers/users.py

from uuid import uuid4, UUID
from typing import List
from fastapi import APIRouter, HTTPException

from app.models import User, UserCreate
from app.db import users_db, user_loans_map

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
