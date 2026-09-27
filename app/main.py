from fastapi import FastAPI
from sqlalchemy import select

from app.db import DbSession
from app.dependencies import unauthorized
from app.models import User
from app.schemas import LoginRequest, TokenResponse
from app.security import verify_password, create_access_token

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/data")
async def get_data():
    return {"message": "Hello World"}


@app.post("/api/data")
async def post_data():
    return {"message": "Hello World"}


@app.post("/api/auth")
async def login(body: LoginRequest, db: DbSession) -> TokenResponse:
    user = db.scalar(select(User).where(User.username == body.username))
    if user is None:
        raise unauthorized()

    password_valid = verify_password(body.password.get_secret_value(), user.password_hash)
    if not password_valid:
        raise unauthorized()

    return TokenResponse(create_access_token(user.id))
