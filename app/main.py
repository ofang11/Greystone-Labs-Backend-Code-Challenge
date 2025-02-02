from fastapi import FastAPI
from app.routers import users

def create_app() -> FastAPI:
    app = FastAPI(title="Loan Amortization API")
    
    app.include_router(users.router, prefix="/users", tags=["Users"])
    
    return app

app = create_app()
