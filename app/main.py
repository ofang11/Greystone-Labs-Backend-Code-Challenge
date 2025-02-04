from fastapi import FastAPI
from app.routers import users, loans
from app.db import init_db
from contextlib import asynccontextmanager

def create_app() -> FastAPI:
    app = FastAPI(title="Loan Amortization API")
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db()
        yield

    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(loans.router, prefix="/loans", tags=["Loans"])
    
    return app

app = create_app()
