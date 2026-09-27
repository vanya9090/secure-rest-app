from time import timezone

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db import DbSession
from app.dependencies import CurrentUser, unauthorized
from app.models import Post, User
from app.schemas import LoginRequest, PostRequest, PostResponse, TokenResponse
from app.security import verify_password, create_access_token

app = FastAPI()


def post_to_response(post: Post) -> PostResponse:
    return PostResponse(
        post.name,
        post.description,
        post.created_at.replace(tzinfo=timezone.utc),
        post.author.username,
    )


@app.get("/api/data", response_model=list[PostResponse])
async def get_data(user: CurrentUser, db: DbSession) -> list[PostResponse]:
    posts = db.scalar(select(Post).options(joinedload(Post.author))).all()
    return [post_to_response(post) for post in posts]


@app.post("/api/data", response_model=PostResponse)
async def post_data(body: PostRequest, user: CurrentUser, db: DbSession) -> PostResponse:
    post = Post(body.name, body.description, user.username)
    db.add(post)
    db.commit()
    db.refresh(post)

    return post_to_response(post)


@app.post("/api/auth", response_model=TokenResponse)
async def login(body: LoginRequest, db: DbSession) -> TokenResponse:
    user = db.scalar(select(User).where(User.username == body.username))
    if user is None:
        raise unauthorized()

    password_valid = verify_password(
        body.password.get_secret_value(), user.password_hash
    )
    if not password_valid:
        raise unauthorized()

    return TokenResponse(create_access_token(user.id))
