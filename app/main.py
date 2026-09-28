from contextlib import asynccontextmanager
from datetime import timezone

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import Base, DbSession, engine
from dependencies import CurrentUser, unauthorized
import models
from models import Post, User
from schemas import LoginRequest, PostRequest, PostResponse, TokenResponse
from security import hash_password, verify_password, create_access_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


def post_to_response(post: Post) -> PostResponse:
    return PostResponse(
        name=post.name,
        description=post.description,
        created_at=post.created_at.replace(tzinfo=timezone.utc),
        author=post.author.username,
    )


@app.get("/api/data", response_model=list[PostResponse])
async def get_data(user: CurrentUser, db: DbSession) -> list[PostResponse]:
    posts = db.scalars(select(Post).options(joinedload(Post.author))).all()
    return [post_to_response(post) for post in posts]


@app.post("/api/data", response_model=PostResponse)
async def post_data(
    body: PostRequest, user: CurrentUser, db: DbSession
) -> PostResponse:
    post = Post(name=body.name, description=body.description, author=user)
    db.add(post)
    db.commit()
    db.refresh(post)

    return post_to_response(post)


@app.post("/auth/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: DbSession) -> TokenResponse:
    user = db.scalar(select(User).where(User.username == body.username))
    if user is None:
        user = User(
            username=body.username,
            password_hash=hash_password(body.password.get_secret_value()),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    elif not verify_password(body.password.get_secret_value(), user.password_hash):
        raise unauthorized()

    return TokenResponse(access_token=create_access_token(user.id))
