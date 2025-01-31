from uuid import uuid4, UUID
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Starter Loan API")

# database placeholders
fake_users_db = {}  
fake_loans_db = {}  
user_loans_map = {} 