from fastapi import FastAPI
from app.routers import users, loans

def create_app() -> FastAPI:
    app = FastAPI(title="Loan Amortization API")
    
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(loans.router, prefix="/loans", tags=["Loans"])
    
    return app

app = create_app()
